#!/usr/bin/env bash
#
# Deploy the LINE book-keeping bot to Google Cloud Run.
#
# Usage:
#   1. cp .env.example .env   &&   fill in the 8 values
#   2. ./deploy.sh
#
# Idempotent: re-run any time. Secrets are created on first run and
# updated (new version) on subsequent runs. Requires: gcloud, an active
# billing-enabled project, and a filled-in .env.

set -euo pipefail

# --- config -----------------------------------------------------------------
PROJECT_ID="${PROJECT_ID:-book-keeping-bot-5975}"
REGION="${REGION:-asia-east1}"
SERVICE="${SERVICE:-book-keeping-bot}"
ENV_FILE="${ENV_FILE:-.env}"

# The 8 config keys the app reads (see app.py, bot.py, sheet.py).
SECRETS=(
  CHANNEL_ACCESS_TOKEN
  CHANNEL_SECRET
  OPENAI_API_KEY
  GOOGLE_API_PROJECT_ID
  GOOGLE_API_PRIVATE_KEY_ID
  GOOGLE_API_PRIVATE_KEY
  GOOGLE_API_CLIENT_EMAIL
  GOOGLE_API_CLIENT_ID
)
# ----------------------------------------------------------------------------

cd "$(dirname "$0")"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERROR: $ENV_FILE not found. Run: cp .env.example .env  and fill it in." >&2
  exit 1
fi

echo ">> Using project $PROJECT_ID, region $REGION, service $SERVICE"
gcloud config set project "$PROJECT_ID" >/dev/null 2>&1

# Read a single key's value from the env file. Only splits on the first '='
# so values containing '=' are preserved; strips surrounding double quotes.
# (Avoids bash 4 associative arrays so this runs on macOS's bash 3.2.)
get_env() {
  local want="$1" line val
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    [[ "${line%%=*}" != "$want" ]] && continue
    val="${line#*=}"
    val="${val%\"}"; val="${val#\"}"
    printf '%s' "$val"
    return 0
  done < "$ENV_FILE"
}

PROJECT_NUM=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")
RUNTIME_SA="${PROJECT_NUM}-compute@developer.gserviceaccount.com"

echo ">> Ensuring required APIs are enabled"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com secretmanager.googleapis.com >/dev/null

# Create-or-update each secret, and grant the runtime SA read access.
SECRET_MAPPINGS=""
for key in "${SECRETS[@]}"; do
  val="$(get_env "$key")"
  if [[ -z "$val" ]]; then
    echo "ERROR: $key is empty in $ENV_FILE" >&2
    exit 1
  fi

  if gcloud secrets describe "$key" >/dev/null 2>&1; then
    printf '%s' "$val" | gcloud secrets versions add "$key" --data-file=- >/dev/null
    echo "   updated secret $key"
  else
    printf '%s' "$val" | gcloud secrets create "$key" --data-file=- >/dev/null
    echo "   created secret $key"
  fi

  gcloud secrets add-iam-policy-binding "$key" \
    --member="serviceAccount:${RUNTIME_SA}" \
    --role="roles/secretmanager.secretAccessor" >/dev/null 2>&1

  SECRET_MAPPINGS+="${key}=${key}:latest,"
done
SECRET_MAPPINGS="${SECRET_MAPPINGS%,}"  # trim trailing comma

echo ">> Deploying to Cloud Run"
gcloud run deploy "$SERVICE" \
  --source . \
  --region "$REGION" \
  --allow-unauthenticated \
  --min-instances 0 \
  --set-secrets "$SECRET_MAPPINGS"

URL=$(gcloud run services describe "$SERVICE" --region "$REGION" --format="value(status.url)")
echo ""
echo ">> Deployed: $URL"
echo ">> Set your LINE webhook URL to: ${URL}/callback"

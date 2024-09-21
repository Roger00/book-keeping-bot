import os
import gspread

from typing import NamedTuple
from booking import Booking, datetime_str

SPREADSHEET_ID = '1xBp1arSbr-qX4t0tQirVtvjdMgR5_R4-WoIezaoquyM'

credentials = {
  "type": "service_account",
  "project_id": f"{os.environ['GOOGLE_API_PROJECT_ID']}",
  "private_key_id": f"{os.environ['GOOGLE_API_PRIVATE_KEY_ID']}",
  "private_key": f"{os.environ['GOOGLE_API_PRIVATE_KEY']}".replace('\\n', '\n'),
  "client_email": f"{os.environ['GOOGLE_API_CLIENT_EMAIL']}",
  "client_id": f"{os.environ['GOOGLE_API_CLIENT_ID']}",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/book-keeping-bot%40fishintosky.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com",
}

def append_booking(b: NamedTuple):
    gc = gspread.service_account_from_dict(credentials)
    wks = gc.open_by_key(SPREADSHEET_ID).sheet1
    wks.append_row([b.datetime, '', b.main_cat, b.sub_cat, b.expense, b.income, b.description], table_range="A1:G1")


def main():
    b = Booking(datetime=datetime_str(), main_cat='食品酒水', sub_cat='午餐', expense=7, income=0, description='鐵男家')
    append_booking(b)

if __name__ == '__main__':
    main()
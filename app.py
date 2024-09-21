import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from sheet import append_booking
from booking import Booking, datetime_str

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    original_message = event.message.text
    append_booking(Booking(datetime=datetime_str(), main_cat='食品酒水', sub_cat='午餐', expense=7, income=0, description=original_message))
    message = TextSendMessage(text=done_message(event.message.text))
    line_bot_api.reply_message(event.reply_token, message)

def done_message(message):
    return f'已記帳: {message}'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

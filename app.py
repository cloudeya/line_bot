from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('5jwDqaZ10rtTgb7srUytNEqcKxZZY5kMFLXrQZeLLh9uVopY+shulBXYxD8FUsuY6qL2nXzvsrw4GcEwy3RA6r1REqpQbNeg5Ov9/h2rdjHa5deyCrFjOVwcQa+uxLA72d9ARbabdetzE6BvCB1c4gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9357353a367b198c0c0bf02fd2c89060')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
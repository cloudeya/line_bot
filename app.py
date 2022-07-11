from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
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
    msg = event.message.text
    r = '你去吃屎'

    if ['貼圖', '想'] in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
        return

    if msg in ['hi', 'Hi', '嗨', '有空']:
        r = '幹嘛，我很忙，你最好不要說廢話'
    elif msg in ['天氣', '吃', '睡', '訂位']:
        r = '關我屁事'
    elif msg in ['你是誰', '兇', '凶']:
        r = '關你屁事，爽'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()
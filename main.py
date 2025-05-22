from flask import Flask,request,abort
from linebot import(
    LineBotApi,WebhookHandler
)
from linebot.exceptions import(
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)
configuration = Configuration(access_token="xoFgrI2e79lUkmKxFrHzD3KUyyacHt26dQMTG19oefBJAum5eez+RB/AcGpi6Vo7nS1VDAR/8KigRwsO72E28UZeMETROan5MfbtGfsH/M+cZ7X5tck7XnfSNoWIXYTK7D1LHTDyzn2phrM+giGt6gdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler('b8a3f2419b4c0ed300091ca280afff8b')

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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )



if __name__ == "__main__":
    app.run()
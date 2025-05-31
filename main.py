import json
import base64
import hashlib
import hmac
import requests
import asyncio
from flask import Flask,request,abort
from models import db
import CRUD

app = Flask(__name__)

with open("./assets/keys.json") as file:
    keys = json.load(file)

app.config['SQLALCHEMY_DATABASE_URI'] = keys["DataBase_URI"]
app.config['SQLALCHEMY_DATABASE_URI'] = keys["DataBase_URI"]
channel_secret = keys["channel_secret"]
chennel_access_token = keys["access_token"]
db.init_app(app)

@app.route("/",methods = ['POST'])
async def callback():
    #獲得請求的簽名
    signature = request.headers.get('X-Line-Signature')

    body = request.get_data(as_text=True)
    #驗證本地簽名和請求簽名是否一致
    try:
        local_signature = base64.b64encode(hmac.new(channel_secret.encode('utf-8'),body.encode('utf-8'), hashlib.sha256).digest()).decode()
        if signature != local_signature:
            abort(400)
    except Exception as exception:
        app.logger.error(f"Signature verification error: {exception}")
        abort(500)  

    try:
        json_data = json.loads(body)
        for events in json_data['events']:
            event_type = events['type']
            app.logger.info(f"處理事件類型: {event_type}")
            if event_type == "message":
                await reply_message(events)   

        return 'OK'
    
    except json.JSONDecodeError:
        app.logger.error("無法解析 JSON 請求主體")
        abort(400)
    
    except Exception as exception:
        app.logger.error(f"處理事件時發生錯誤: {exception}")
        abort(500)  

async def reply_message(request):
    with open("./assets/conversations.json") as conversations:
        conversation = json.load(conversations)
    headers = {'Authorization':'Bearer ' + chennel_access_token,'Content-Type':keys['content_type']}
    message = request['message']
    reply_token = request['replyToken']
    if message['type'] == "text":
        if message['text'] == conversation["add_task"]:
            reply_message = {
                "replyToken":reply_token,
                "messages":
                [
                    {
                        "type":"text",
                        "text":conversation["response_add_task"]
                    }
                ]
            }
            await CRUD.Task_Event(request["source"]["userID"],True,False)
        else:
            reply_message = {
                "replyToken":reply_token,
                "messages":
                [
                    {
                        "type":"text",
                        "text":message['text']
                    }
                ]
            }
        try:
            requests.post('https://api.line.me/v2/bot/message/reply',headers=headers,data=json.dumps(reply_message)) # requests 使用 data 參數傳遞 JSON 字串
            app.logger.info(f"事件類型:{message['type']}")
            app.logger.info(f"回應token:{message['replyToken']}")
        except Exception as E:
            app.logger.error(f"錯誤訊息!{E}")
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
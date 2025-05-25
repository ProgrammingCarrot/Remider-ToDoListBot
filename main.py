import json
import base64
import hashlib
import hmac
import requests
from flask import Flask,request,abort

app = Flask(__name__)

with open("./assets/keys.json") as file:
    keys = json.load(file)

channel_secret = keys["channel_secret"]
chennel_access_token = keys["access_token"]

@app.route("/",methods = ['POST'])
def callback():
    #獲得請求的簽名
    signature = request.headers.get('X-Line-Signature')

    body = request.get_data(as_text=True)
    request = json.loads(body)
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
        reply_message(json_data)   

        return 'OK'
    
    except json.JSONDecodeError:
        app.logger.error("無法解析 JSON 請求主體")
        abort(400)
    
    except Exception as exception:
        app.logger.error(f"處理事件時發生錯誤: {exception}")
        abort(500)  

def reply_message(request):
    headers = {'Authorization':'Bearer ' + chennel_access_token,'Content-Type':keys['content_type']}
    if request['events']['type'] == "message":
        message = request['events']['messgae']
        reply_token = request['events']['replyToken']
        reply_message = {
            "replyToken":reply_token,
            "messages":
            {
                "type":"text",
                "text":message
            }
        }
    else:
        return 0
    requests.post('https://api.line.me/v2/bot/message/reply',headers=headers,data=json.dumps(reply_message))

    


if __name__ == "__main__":
    app.run()
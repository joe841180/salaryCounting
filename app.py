from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import json

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "cwzYEsTdi7hp0XkTLFQcX80E+4Zub/rmDIZHuIS85GjVhoXy9nvug/PVjhUsoOEi3akOhE7VTcyBSenY+8AyS+kquCBl2FbJ5r6px8JC+VabC3ye85lMcjS1I9Xhzamk77QtqGccGOdokZXO/NsLDAdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "adcdb4d9df7e94f2979c6053be670575"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 讀、存檔
class handlingFile:
    salaryData = "salaryData.json"
    sample = {
        "workDays":[
                {
                "date":"1004",
                "workTime":"0800-0930",
                "task":"1.測試\n2.測試",
                "m-油錢":"100"
            }
        ],
        "config":{
            "name":"", 
            "wage":"180", #時薪
            "healthCare":False, #健保
            "laborInsurance":False, #勞保
        }
    }
    def read(self):
        with open(self.salaryData,"r") as f:
            data = json.loads(f.read())
            return data

    def write(self, data):
        with open(self.salaryData,"w") as f:
            data = json.dumps(data)
            f.write(data)

# def inputDate(message):
#     data = handlingFile.read() #讀取
    
#     if message.find(""):
#         data[""] = ""
    
#     handlingFile.write(data)#寫入





# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # message = TextSendMessage(text=event.message.text)
    message = event.message.text

    # 儲存日期、計算時數
    if message == "123":
        res = message
    else:
        res = "error"

    # res = "test"

    # 回傳
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=res))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import json
import psycopg2

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "cwzYEsTdi7hp0XkTLFQcX80E+4Zub/rmDIZHuIS85GjVhoXy9nvug/PVjhUsoOEi3akOhE7VTcyBSenY+8AyS+kquCBl2FbJ5r6px8JC+VabC3ye85lMcjS1I9Xhzamk77QtqGccGOdokZXO/NsLDAdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "adcdb4d9df7e94f2979c6053be670575"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 讀、存檔
class handlingData:

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
    def __init__(self):
        conn = psycopg2.connect(database="資料庫名稱",
            user="uqelofwpevaxsf",
            password="76d0dc1ff97412ed81c65785829d463e2b2f9cd453911647deab9a509d6ad87f",
            host="ec2-23-20-140-229.compute-1.amazonaws.com",
            port="5432")
        self.conn = conn
        self.cursor = conn.cursor()
        print("Opened database successfully")

    def write(self, data):
        with open(self.salaryData,"w") as f:
            data = json.dumps(data)
            f.write(data)

    # 建立資料表
    def creatDB(self):
        cursor = self.cursor()
        cursor.execute("CREATE TABLE userdata (id serial PRIMARY KEY, name VARCHAR(50), userid VARCHAR(50));")
        print("Create table successfully")
        cursor.close()

    # 寫入資料
    def write(self):
        cursor = self.cursor()
        cursor.execute("INSERT INTO userdata (name, userid) VALUES (%s, %s);", ("小明", "a123456"))
        cursor.execute("INSERT INTO userdata (name, userid) VALUES (%s, %s);", ("小王", "b654321"))
        cursor.execute("INSERT INTO userdata (name, userid) VALUES (%s, %s);", ("小華", "c987654"))
        print("Inserted 3 rows of data")
        self.conn.commit()
        cursor.close()

    # 讀取資料
    def read(self):
        cursor = self.cursor()
        cursor.execute("SELECT * FROM userdata;")#選擇資料表userdata
        rows = cursor.fetchall() #讀出所有資料

        for row in rows:   #將讀到的資料全部print出來
            print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

    # 更新資料
    def update(self):
        cursor = self.cursor()
        cursor.execute("UPDATE inventory SET userid = %s WHERE name = %s;", ("d123789", "小明"))
        self.conn.commit()
        print("Updated 1 row of data")
        cursor.close()

    # 刪除資料
    def delete(self):
        cursor = self.cursor()
        cursor.execute("DELETE FROM userdata WHERE name = %s;", ("小華",))
        print("Deleted 1 row of data")
        self.conn.commit()
        cursor.close()



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
    db = handlingData()

    # 儲存日期、計算時數
    if message == "123":
        res = "error"
    else:
        res = message

    # res = "test"

    # 回傳
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=res))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

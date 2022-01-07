from __future__ import unicode_literals
from typing import Sized
import json
import urllib.request as request
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import configparser
import random

from hello import getweather
from keep_alive import keep_alive
app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


cities = ['基隆市', '嘉義市', '臺北市', '嘉義縣', '新北市', '臺南市', '桃園縣', '高雄市', '新竹市', '屏東縣',
          '新竹縣', '臺東縣', '苗栗縣', '花蓮縣', '臺中市', '宜蘭縣', '彰化縣', '澎湖縣', '南投縣', '金門縣', '雲林縣', '連江縣']


@handler.add(MessageEvent, message=TextMessage)
def prettyEcho(event):

    sendString = ""
    if '天氣' in event.message.text:
        sendString = event.message.text
        city = sendString[3:]
        city = city.replace('台', '臺')
        if(not (city in cities)):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="查詢格式為: 天氣 縣市"))
        else:
            weather = getweather(city)
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text=city + '未來 36 小時天氣預測',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://i0.wp.com/kkplay3c.net/wp-content/uploads/2020/08/weather-taiwan.png',
                            title='{} ~ {}'.format(
                                weather[i][0:14], weather[i][15:29]),
                            text='{}\n天氣狀況 {}\n降雨機率 {} %'.format(
                                weather[i][30:41], weather[i][42:45], weather[i][45:58]),
                            actions=[
                                URITemplateAction(
                                    label='詳細內容',
                                    uri='https://www.cwb.gov.tw/V8/C/W/County/index.html')
                            ]
                        )for i in range(3)
                    ]
                )
            ))

    elif "擲筊" in event.message.text:
        sendString = divinationBlocks()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=sendString))
    elif "抽簽" in event.message.text or "抽" in event.message.text:
        sendString = drawStraws()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=sendString))
    else:
        sendString = event.message.text
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=sendString))


def divinationBlocks():
    divinationBlocksList = ["笑杯", "正杯", "正杯", "笑杯"]
    return divinationBlocksList[random.randint(0, len(divinationBlocksList) - 1)]


def drawStraws():
    drawStrawsList = ["大吉", "中吉", "小吉", "吉", "凶", "小凶", "中凶", "大凶"]
    return drawStrawsList[random.randint(0, len(drawStrawsList) - 1)]


# if __name__ == "__main__":
  #  app.run()
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

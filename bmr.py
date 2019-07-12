# -*- coding: utf-8 -*-
import re
import urllib.request

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

SLACK_TOKEN = 'xoxb-678301475330-678323565299-4tD09q3pjLTf9tJPrhpadLCj'
SLACK_SIGNING_SECRET = '7781b68227520fb3c819742b14b333e5'

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)


# 크롤링 함수 구현하기
def BMR(text):  # 남/나이/키/몸무게/
    gender = text.split('/')[0]
    age = int(text.split('/')[1])
    height = int(text.split('/')[2])
    weight = int(text.split('/')[3])
    if '남' in gender:
        bmr = 66.47 + (13.75 * weight) + (5 * height) - (6.76 * age)
    elif '여' in gender:
        bmr = 655.1 + (9.56 * weight) + (1.85 * height) - (4.68 * age)
    final = '하루 기초 대사량은 '+str(bmr)+'입니다!'
    return final


# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    keywords = BMR(text)
    slack_web_client.chat_postMessage(
        channel=channel,
        text=keywords
    )


# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)

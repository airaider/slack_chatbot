# -*- coding: utf-8 -*-

import random
import re
import os
from flask import Flask
from slack import WebClient
from slack.web.classes import extract_json
from slack.web.classes.blocks import ImageBlock, SectionBlock
from slackeventsapi import SlackEventAdapter


from config import *

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)


def joke(text):
    if 'ㅠ' in text:
        head_section = SectionBlock(
            text='회원님~ 울면 근손실 일어나요~\n울지마요~'
        )
        block1 = ImageBlock(
            image_url='http://bitly.kr/8iTBeh',
            alt_text='이미지 오류'

        )
        return [head_section, block1]
    elif '배고파' in text:
        head_section = SectionBlock(
            text='이걸 보고도 밥이 목구녕으로 넘어가요?\n단식하세요 회원님~'
        )
        block1 = ImageBlock(
            image_url='http://bitly.kr/PopTfn',
            alt_text='이미지 오류'

        )
        return [head_section, block1]
    elif '언더아머' in text:
        head_section = SectionBlock(
            text='언더아머는 3대 500치는 회원님들만 착용 가능합니다.\n단속걸리지 않게 조심하세요 회원님~'
        )
        block1 = ImageBlock(
            image_url='http://bitly.kr/Q0ANbf',
            alt_text='이미지 오류'

        )
        return [head_section, block1]
    else:
        a = random.randint(1, 4)
        if a == 1:
            head_section = SectionBlock(
                text='운동만이 살길입니다 회원님~\n오늘도 식단관리 화이팅~!'
            )
            block1 = ImageBlock(
                image_url='http://bitly.kr/f9TIze',
                alt_text='이미지 오류'

            )
            return [head_section, block1]
        elif a == 2:
            head_section = SectionBlock(
                text='운동은 마음가짐입니다 회원님~\n열심히 노력하셔야 해요!'
            )
            block1 = ImageBlock(
                image_url='http://bitly.kr/5sNxFM',
                alt_text='이미지 오류'

            )
            return [head_section, block1]
        else:
            head_section = SectionBlock(
                text='몸도 중요하지만 회원님~\n몸완얼인것도 아시죠??'
            )
            block1 = ImageBlock(
                image_url='http://bitly.kr/3bBR3R',
                alt_text='이미지 오류'

            )
            return [head_section, block1]


def setBaseUser(info,user):
    # 성별/나이/키/몸무게
    temp = info.split('/')
    gender = temp[0].split(' ')[1]

    with open(user, "w") as userfile:
        if gender == "남자":
            base = 66.47 + (13.75 * int(temp[3])) + (5 * int(temp[2])) - (6.76 * int(temp[1]))
        else:
            base = 655.1 + (9.56 * int(temp[3])) + (1.8 * int(temp[2])) - (4.68 * int(temp[1]))

        userfile.write(str(round(base)) + "\n")
    return round(base)


def getBaseUser(user):
    with open(user, "r") as userfile:
        base = float(userfile.readline().replace('\n', ''))

    return base


def sumOfcal(user):
    with open(user, "r") as userfile:
        sumcal = 0.0
        for idx, line in enumerate(userfile):
            if idx == 0:
                continue
            sumcal += float(line.split('/')[1].strip())

    return sumcal


def findFood(food_name):
    with open("food5.csv", 'rt', encoding='UTF8') as file:
        kal = 0
        for i in file:
            if food_name == i.split(',')[0].strip():
                kal = float(i.split(',')[1].strip())
        if kal == 0:
            head_section = SectionBlock(
                text="*" + food_name + "*" + " 의 칼로리에 대한 정보는 없네요 회원님 ㅠㅠ\n다른 음식을 찾아보시겠어요??"
            )
            block1 = ImageBlock(
                image_url='http://bitly.kr/eeFDFw',
                alt_text='이미지 오류'
            )
            return [head_section, block1]

    head_section = SectionBlock(
        text="*" + food_name + "*" + " 의 칼로리는 " + "*" + str(kal) + "*" + " 이네요.\n생각보다 높아서 걱정인데....\n정말 드시겠어요 회원님...??"
    )
    block1 = ImageBlock(
        image_url='http://bitly.kr/Q8DSXA',
        alt_text='이미지 오류'
    )
    return [head_section, block1]


def eatFood(food_name,user):

    with open("food5.csv", 'rt', encoding='UTF8') as file:
        kal = 0
        for i in file:
            if food_name == i.split(',')[0].strip():
                kal = float(i.split(',')[1].strip())
        if kal == 0:
            head_section = SectionBlock(
                text="*" + food_name + "*" + " 의 칼로리에 대한 정보는 없네요 회원님 ㅠㅠ\n다른 음식을 찾아보시겠어요??"
            )
            block1 = ImageBlock(
                image_url='http://bitly.kr/eeFDFw',
                alt_text='이미지 오류'
            )
            return [head_section, block1]

    with open(user, "a+") as userfile:
        data = food_name + "/" + str(kal) + "\n"
        userfile.write(data)

    if sumOfcal(user) > getBaseUser(user):
        head_section = SectionBlock(
            text="*" + food_name + "*" + " 을 먹어서 지금 " + "*" + str(
                round(sumOfcal(user) - getBaseUser(user))) + "*" + " 칼로리를 초과했습니다.\n 회원님 갑시다, 진실의 방으로"
        )
        block1 = ImageBlock(
            image_url='http://jjalbox.com/jjalbang/jbox1Gd.jpg',
            alt_text='이미지 오류'
        )
        return [head_section, block1]

    a = round(sumOfcal(user) / getBaseUser(user) * 100)
    if a < 25:
        t ="*" + food_name + "*" + " 의 칼로리는 " + "*" + str(kal) + "*" + " 입니다 회원님~~.\n" + "누적된 칼로리는 " + str(
            round(sumOfcal(user))) + " / " + str(
            getBaseUser(user)) + " *-------" + str(
            round(sumOfcal(user) / getBaseUser(user) * 100)) + "%" + "*" + " 입니다.\n잘 하고 계시니까, 칼로리 안넘치도록 조심하세요!"
        b = 'http://bitly.kr/f8gS2k'
    elif a < 50:
        t ="*" + food_name + "*" + " 의 칼로리는 " + "*" + str(kal) + "*" + " 입니다 회원님~~.\n" + "누적된 칼로리는 " + str(
            round(sumOfcal(user))) + " / " + str(
            getBaseUser(user)) + " *-------" + str(
            round(sumOfcal(user) / getBaseUser(user) * 100)) + "%" + "*" + " 입니다.\n아오, 회원님 때릴뻔 했네...\n 회원님 적당히 먹으세요\n부탁드리겠습니다~"
        b = 'http://bitly.kr/USshUs'
    elif a < 75:
        t = "*" + food_name + "*" + " 의 칼로리는 " + "*" + str(kal) + "*" + " 입니다 회원님.\n" + "누적된 칼로리는 " + str(
            round(sumOfcal(user))) + " / " + str(
            getBaseUser(user)) + " *-------" + str(
            round(sumOfcal(user) / getBaseUser(user) * 100)) + "%" + "*" + " 입니다.\n회원님... 상큼하게 터져볼래요?\n지금 칼로리 위험위험 합니다 ^^"
        b = 'http://bitly.kr/We2Rny'
    elif a < 100:
        t = "*" + food_name + "*" + " 의 칼로리는 " + "*" + str(kal) + "*" + " 입니다 회원님.\n" + "누적된 칼로리는 " + str(
            round(sumOfcal(user))) + " / " + str(
            getBaseUser(user)) + " *-------" + str(
            round(sumOfcal(user) / getBaseUser(user) * 100)) + "%" + "*" + " 입니다.\n회..회원님... \n아 말리지 말아봐요..!!"
        b = 'http://bitly.kr/5zTLj6'
    head_section = SectionBlock(
        text=t
    )

    block1 = ImageBlock(
        image_url=b,
        alt_text='이미지 오류'

    )
    return [head_section, block1]


def getExercise(text):
    temp = text.split('/')
    dic = {}

    if temp[1] == '?':
        return "우리 회원님이 어떤 운동을 좋아할지 몰라서 다 준비해봤어요 ~ \n 운동/고강도\n운동/저강도\n운동/등운동\n운동/가슴운동\n운동/하체운동\n운동/어깨운동\n운동/유산소\n*운동/치킨 먹고*\n*운동/야식 먹고*\n운동/스트레칭\n운동/홈트레이닝\n운동/플란체"
    return {'고강도': 'https://youtu.be/PJR8xQc_evY',
            '저강도': 'https://youtu.be/dmHe5TWstkU',
            '등운동': 'https://www.youtube.com/watch?v=fjswoq9uv90',
            '가슴운동': 'https://www.youtube.com/watch?v=yf0qL-JoYVQ',
            '하체운동': 'https://www.youtube.com/watch?v=fkpkqWbGdKs',
            '어깨운동': 'https://www.youtube.com/watch?v=8U89oCO5Gg4',
            '유산소': 'https://youtu.be/3VouSaW_LPw',
            '치킨 먹고': 'https://youtu.be/kPnujJxEYHg',
            '야식 먹고': 'https://youtu.be/gHum0RnB7Lg',
            '스트레칭': 'https://youtu.be/2LyDkE7sDec',
            '홈트레이닝': 'https://youtu.be/qf5OnPm34YI',
            '플란체': 'https://youtu.be/ucUQ5yyD7mk'}.get(temp[1], '내가 모르는 운동 물어보지 말랬지?')


def intro(uu):
    head_section = SectionBlock(
        text="안녕하세요 "+uu+" 회원님~~\n회원님의 식단과 운동을 책임질 마블리입니다\n우선은 회원님의 기본 정보를 입력해볼까요??\n아래 예시 처럼 입력해주세요 회원님~~\n사랑합니다~\n(ex : 남자(성별)/21(나이)/170(키)/60(몸무게))"
    )
    block1 = ImageBlock(
        image_url='http://bitly.kr/Kc1l5h',
        alt_text='이미지 오류'

    )
    return [head_section, block1]


# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]
    user_di = event_data["event"]["user"]
    user_id = 'C:/Users/student/PycharmProjects/untitled/db/'+user_di+'.txt'
    uu='<@'+user_di+'>'
    if 'admin' in text:
        keywords = uu
    elif 'help' in text:
        keywords = "앱 초기 실행은 @test 을 mention\n정보 기입은 성별/나이/키/몸무게  *ex:남자/24/176/65 * 형식으로 기입\n음식 칼로리 검색은 *검색/음식명*\n먹은 음식 계산은 *음식/음식명*\n운동 관련 유튜브 영상 시청은 *운동/?*\n하루 권장 칼로리 안넘기도록 주의하세요!"

    elif "운동" in text:
        keywords = getExercise(text)
    elif "검색" in text:
        food = text.split('/')[1]
        keywords = findFood(food)
        slack_web_client.chat_postMessage(
            channel=channel,
            blocks=extract_json(keywords)
        )
        return
    elif re.search(r"남자|여자", text):
        keywords = "네 "+uu+"회원님~~\n회원님께서는 하루 권장 칼로리가 " + "*"+str(setBaseUser(
            text, user_id))+"*" + " 이네요~\n이 이상 드시면 이 이상 드시면 살이 디룩디룩 찔테니 절--대 넘기시면 안됩니다!!\n앞으로는 음식먹기 전에 저한테 항상 검사를 맡아야 합니다!"
    elif "음식" in text:
        food = text.split('/')[1]
        keywords = eatFood(food,user_id)
        slack_web_client.chat_postMessage(
            channel=channel,
            blocks=extract_json(keywords)
        )
        return
    elif len(text) == 12:
        keywords = intro(uu)
        slack_web_client.chat_postMessage(
            channel=channel,
            blocks=extract_json(keywords)
        )
        return
    else:
        keywords = joke(text)
        slack_web_client.chat_postMessage(
            channel=channel,
            blocks=extract_json(keywords)
        )
        return

    slack_web_client.chat_postMessage(
        channel=channel,
        text=keywords
    )
    return


# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002)

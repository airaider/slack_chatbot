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
            image_url='https://lh3.googleusercontent.com/hguAuf5QNQrXgUcpzHiZvc8nATE4abjsm36RutYY2RmoRiunaPQYrtVu6bdabJOiAsGVYhNddP6Jwn9oFaBCOcd4yXyeiCK2jMQPSPNSY3Xf-y92L4ZPBwXUk2Sgy_PlvUrhcgnQaDdD5j2Q6GrRLPuFgNRa_B5eDeU8bloS7DiX7-Z-OIwQJFZPYau8bBiplhV6Qb1JEjEJm_9nOTAvuAYoRCGArs6_lFf53oAssxooJnuEnVu8L7VPfLzEnvovK65lvgHaFL2_-voZ5k7uF_vQGVgoSBXJgICOi9afhbKGfy5nqW6rvSYQGQBcKxuhzLAifkZwPfze93a7jLLjlh5uOjd_e_qsF0yAXlEGBqd3k1QehUVYjkZRdkc7_ULxsaWzDgQ1jtu0SYnwlM-WcdGRWf9kayGs3s-_yY0rjn6-TlTI0ip5EFhiVA-oqC1be5LCwGeEvxGCvmZgWvzE0LK8J90grXiINXxGF0xsAECO8-t3MU0eLPDzPazftQRKNMObEfBj5f0mA41n1ergumMc-iliJzx2M4_tN22mIUsq8nM7fP5AkULVrQHs7i_6dC1PE5ua3nxQLMHA8lc_-rIJln3Rqizn27sVJREyuW50hFHlQKfSzzfKT_0_IgYvdpfBO_E6AduGYrl3oXFf0jxPe9cIABk=w1080-h566-no',
            alt_text='이미지 오류'

        )
        return [head_section, block1]
    elif '배고파' in text:
        head_section = SectionBlock(
            text='이걸 보고도 밥이 목구녕으로 넘어가요?\n단식하세요 회원님~'
        )
        block1 = ImageBlock(
            image_url='https://lh3.googleusercontent.com/8coAcbfuPVGQusuhukNzXV5QyIjNIQN2TEgBEMGjk7OgGtJBGMoQlf6mYQB8fM5_U_O-q6EOhecKm7k4f5jMiLrJ8gsK3L3PLc9EZFcFdhJfWZ0lEnPee-BN7oOkV4_cwuEjvGIA33jMn0-t8I9bhfm3KwvEAYh7gWnCTdPt7xKL3xEhs2VPLQ3c8D4Nzkc1RExG55s6rhtLCU7Tx7G-2WIOghLbuOpdNL1aVejGXBTBnSU3CEN-7ElUo7yprjb7Y6dxRc0JpZHrveKH_mc0LU5-EUR4LERA2fImwtbpI0-jGBGLOZYzkGOyh04uVIHXfHuNe5yh9CAcNkizPJ3HgDr6yujtyA9Vw5XMgM5GOascxYvM-axlc7k2SUb0478XcipU6ErIS9V8_OiytFNcbJq4rcWWt55VwxUJXFWblf5-cXWapvADG-DRBc2_LJzTrCyC0Yr2cIjGR3PrN4DKIxj-d1TmXXCZx9q3Dbhf2YAY0Qi2jPYcJI2iwRZHpjrKOGQuEpe7a8-NmfvDgxYp5_GEc-JvDg9MQftGS9r3RnF5EmKTpa3T38CgWSAgx1pzcDY6VExt5pwqG5dZp0dNvokCqhw95dqjMRejkRfSTdZ2GwxlWAvLw6vvYXhigSWmSGg2CePCENNnY5IZfXcaXTWUh2AUPL0=w562-h555-no',
            alt_text='이미지 오류'

        )
        return [head_section, block1]
    elif '언더아머' in text:
        head_section = SectionBlock(
            text='언더아머는 3대 500치는 회원님들만 착용 가능합니다.\n단속걸리지 않게 조심하세요 회원님~'
        )
        block1 = ImageBlock(
            image_url='https://lh3.googleusercontent.com/dZtOqOrDykNsxJDCb1JePrlnUHRJ6KAZ5kBTdhObypu6kEi-kFYo2nJYdCmlHKnPPfSHxgjSGqA5fVju6YVh6Fq8G6BeFkx7s-l42mkTG0j8GseW-_NKLfXv1f0gKLzHdyq4SuvY5BIJCVpmWdzPK_m6W64uZHNQJaFoOQOSXbwEYdugI1aMFWnZiPW3a3lvFZGAZ9gf9chKumwdxDLs8hb1TMsjlnP-l3OXGeMvd0cZUXxGDPtwfJ-7UWzbEelwpCVC6PynqdMNBcJ-aO92fpx7H6YxCTa8mkeNvKjF7N9UXSeOxkjwv9nCw2vxJdRm7apLXIjPQuCnf70KBtj7yE-Cai4Ri-T2Z1l4sJL7qXU-TKf8jHPmmL5Q1LYgszkuU5XWJsyx5AB2eMUpBhxPRFqdVpK1kJ7cv8i0Z1fo-rL8AZV5CrvLCajY0UWefjbJPNgxdcTKjahuX1nmANUEdLl12pz6X-NXPoYrays12hFjdUVs4jf3L8lkvwQpgLML4tyG_94KBj3shr6885TuWMJ8bzXrX4-wExhpkb83bQ5Y6Fx7T-98zmzFv9GUgDJN0uYyDyxfNdIEqU9OVTz8IgEOJwBEn1dhYCpSwEDfK6ytPfb65MuCOM3rF-OccVIlKy3iRfoqn0lTTh9nbgrZVALFuBqjVG4=w480-h360-no',
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
                image_url='https://lh3.googleusercontent.com/WtzRAuX3FBFWkaJ9f_V9pz4SZeaF0eKtLMBuzG3UQUGMpPwwXDuJRBCm-ywHPXtnseBoQHJY0VL403dRWeBzeC1cbqg-_sonFaboyMbdUE3PK7Dkk7wg6ttB62zU1KcsDQDN5CkBwD8p-46Zrhrbzx6YLj_PEMk8vT3-H11Yv_XRz6liNpOctV_b-ZdSxmxm7ASrbzr2alRXi7LYOc4cBwTTRXSx5RuLsC0YexIY2dbkvctU-uVAwE8D1pVy4oyDhO_JDFvUJ_23tW5PC9hZSxlFfFZbs2Us6JOgJXQTAuV6_v9-ttElhZ3HdmnMhshjs9nOB_msBFIcgFOJiVXbyVHpq_C9z9Me7O3HztaKI2NKStevMVROwVE4Y4LnkAYXPk2GqOIpBHQmOXltIPguu-bWwWfIE7HLFiZ9hPYJdyFr3ocfhxbp6XASnsTKnT8Uo-qKGJvb4UkYSO9snqZBlMqiODjbcxNX5ER2MTyvAoHJCvVrWo_pYNwJmAAjBUR476xr8O8lJLu6_4mJAjx7D1HH6KkV98kedOBI8ZCoXwBbWNLjRJ0GdzLcBlIrDXnf1dsi_UVgUvQ4SN4CffrzlSIFopeAfaCQDPCwVJ4-VKvwg42rkjZGfmOovlgeAq2x9NporUOBkY45BXJ9Z4xLYAUbPsJQElM=w300-h168-no',
                alt_text='이미지 오류'

            )
            return [head_section, block1]
        elif a == 2:
            head_section = SectionBlock(
                text='운동은 마음가짐입니다 회원님~\n열심히 노력하셔야 해요!'
            )
            block1 = ImageBlock(
                image_url='https://lh3.googleusercontent.com/sfUnnQaoAysIBzSBkrLbZwO3bUThjF9E0Lb2JxB-QyJ6OgLo5RfGrAubkZKvm31b-zWyhYzsEM_V3_pyrrh_vvjNymptF6BF7YrfvUAdp5VNCBW76ZpOd06-VCjXpe0de0X0jlW6akvPwKxb0UNrkrIIY9ys8cFtMehj004xv7tsTycUXRiwPr83PLFYmUI9d1jCiUfM0HpBntUSO6Kc76PjPI-mNPaxrakpqlvTuPDaxbohioDQFTnJpkTUX6ZmeLX2Tz0M4viIhIFiv3ph5rONmeM_LxYbAc77l_9Y8EeRhdDBCNjxahyquZt4AAH4ots0Yf2FNbxFXsFQph7_UT3PddapAwb0x5rOZflttIxoDiaWbuPWP3uPVM3BW94VsDt6NE6SCHIT0_pnRtr2AYdGQ5VlI2EQ4ocN-ueH89WDOLuZh5GErO77uJTdp9V1rGJhU6Dyvqy19_xV0Udd9Byf9QcQsQ95d7BOHS92FroJFRk6E5igmRNe8VTsJgxX_Fu5Dz-XcaVVpb86BmlaedE10v-ZautFloH9DR-GLjeKhwc1ZTUB5aihno_SWN7h4bAs-krDYZ0TChFV8Q_YsxhSrV43zVK_20oIBFm7YYLWt1PzP-rF1TkQSkONOkbuc5f_F1gskOOBjL_wqRCakZ5lKpB6GCQ=w1200-h675-no',
                alt_text='이미지 오류'

            )
            return [head_section, block1]
        else:
            head_section = SectionBlock(
                text='몸도 중요하지만 회원님~\n몸완얼인것도 아시죠??'
            )
            block1 = ImageBlock(
                image_url='https://lh3.googleusercontent.com/MYuP8tgvOl03wNHV0hpwXc_Lbd8937HIzKzmfO1Z2mZdaKuaNUjUkRt5v2j9hvq7R-yS1M6XTcQvE5SQ9lF1fy3YgLyX5E60pbuhzp_e5D6MDzXixj-k-q2-JBKc-_NfClsOwW3fKS2Crh-2vdjhDSjvVz9QrFyNcsBp3wHVHoomzhtnie9rQqN5lJKxmQjOzeO_2eqyDAimS9udOrhQruokCb3wwfNTe9x9R01KeBCR1DzGDcuhZeCvgQ6ae9tTmSSYr1AtDCxpGPN62e9xgPx8uf6zCtiYJkPwzqcW37363fYb9v0I9Ua2O6MgMicDt1dfba18zguP4sGmr3kpzDh6q4MKSOSwSN0XBDRUfZo2GbtZ5ZQj__s3c7Rv5p-WvwQQLBnM-uvx0WOmnyFEOO47UdJg3XU1AYMsb5gmtaIN7x3dhVxPBiuku1KWwZC1NcD59oHc9Gxk1q5LiykC-iDTlo5FKAC1WYvbDFZn2uhHwGJDQuvWEb5Qcpnf2WkLM4vfeAE1dm_LUk_KdvZue6Hs6jv_3BmbMAdxSWGUHA2hGLqrmlxIM9RR4KFVWN2gcqNZO19tz9y74U3uMdx2N7xmuepFF_WTnSOf4nu8QNbpVSV2wLLnaJRmzy5iLDYTGL77S9iNHIG-JtXd2COq1AmVwvFXKE4=w188-h268-no',
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
                image_url='https://lh3.googleusercontent.com/9JbVrSd_VM5gtIES8nV1hFv9INJ5aOatExiwP9BOMjRL5StZKojJiZwNjvzyO5fJdToeh9fuoNEZwOkVEzWIj0znMJs3zVJtU__dfTzeQpBb72tI7v_H6UL654Up-Dz8UlvRg1QtCoE_qFR7_rjp60j-uVnw6H7v60nOc5sLzo0cFdxWJmo9NMvxPdHKVCsqLBLVresLeyL6Ulndh2ayShzKb4DCHnbH2kYBVQJ7HFNLuN_8wU5Z9lc0D97ppiX9awxoXqMgqvvS9epaBeg5Jn0KNEM4BdyAxTqbZcakZdCD3s8HjwJ0K0BOrbugNcKI9GPwsJ0Zjzoq9LUb6Yz8mJpoVAuMKMPJemI0NXCPLLzisjNzR6kCLI7Rc2BHSyIJkc4aEGWCMBTFKtd54SIQuv9lkCvK3kTOKfjS39G1-YDfGfWcbgU83l6TMPxOMQlU7l6328vd_QXOWe8c4WVv2Mh6toJnWXCwIwCghaxMGmqc5qwj96gUlBir-l1CooBPp1Ln-iurmhc1CeySEsCyfS2wa0Xz4AN8VNwMwOHHTJT6fgepWfZIrqby57GsyJ3fuBRekvQIkK_XIQmBYGnwmwGdcBF46j3bSMuAals0PraWUv8NptJaB2U48eGJfbV3H3NnqCniTyhkSuzklrnjjcN8F-Pukus=w530-h375-no',
                alt_text='이미지 오류'
            )
            return [head_section, block1]

    head_section = SectionBlock(
        text="*" + food_name + "*" + " 의 칼로리는 " + "*" + str(kal) + "*" + " 이네요.\n생각보다 높아서 걱정인데....\n정말 드시겠어요 회원님...??"
    )
    block1 = ImageBlock(
        image_url='https://lh3.googleusercontent.com/Jrn3NDI3XofgtKIMK-_lyY7vQn2Na6GvEr4DCPNtEh-bTb7IWlVAuGw3ypduDBgAgcs5h1ukAHrPhVaGf62CZ62896nfLqWYsrpr27_Y_R7FzezsWA0pd4x4g4PWdCD5uKRyUIyDfo0padPBrSNNjdD1CoBhZVibqueexsMXLX3iqv7tiyULWnDB-Ll6y7VgIGgo4iw7ONEbL8VoQ9apWbbg-Koo9mNZhKMRiRSUJAeSe6chB8NSqzurj7Np7ZpORa45pTb4iR5fgr4j3nQGVNccGuJ_2H6yDtpoPNuPhPaDzBtcw99djbqGESM3QYNRPnvu3s3vWmQw7eQA9ZRmSv51qCoj78e3udOkRCqC13RAmfVVsEGVu06AZNcwZQ_pu4BbImM01-OO0iu9OdX4gkM3dTUHlka4BdKfl4oGOp8gU986jkKNComnse0Ex1SD6qDEg_MTzDQ-yEPdkCVr0ZXC6Guj5bYJLDFqFoDK5F0pHKjt7YJcqsyZFxHgFi-dGtSKddv4NERsVUWt2_I6OHUNZaGTMGY6ctdXN7zZ99sep64kGE_EZ1m0rtmT3Qgf8k6AjlX1wdlwQpOiHlYIZz0V7P3V7YA9ZTh9LCeekQrtcp0k2ytrt4fgnTak6gGn6xpzbRAE8FCjcRtJSV9k63PHmcuY4LQ=w640-h960-no',
        alt_text='이미지 오류'
    )
    return [head_section, block1]


def eatFood(food_name,user,uu):

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
                image_url='https://lh3.googleusercontent.com/9JbVrSd_VM5gtIES8nV1hFv9INJ5aOatExiwP9BOMjRL5StZKojJiZwNjvzyO5fJdToeh9fuoNEZwOkVEzWIj0znMJs3zVJtU__dfTzeQpBb72tI7v_H6UL654Up-Dz8UlvRg1QtCoE_qFR7_rjp60j-uVnw6H7v60nOc5sLzo0cFdxWJmo9NMvxPdHKVCsqLBLVresLeyL6Ulndh2ayShzKb4DCHnbH2kYBVQJ7HFNLuN_8wU5Z9lc0D97ppiX9awxoXqMgqvvS9epaBeg5Jn0KNEM4BdyAxTqbZcakZdCD3s8HjwJ0K0BOrbugNcKI9GPwsJ0Zjzoq9LUb6Yz8mJpoVAuMKMPJemI0NXCPLLzisjNzR6kCLI7Rc2BHSyIJkc4aEGWCMBTFKtd54SIQuv9lkCvK3kTOKfjS39G1-YDfGfWcbgU83l6TMPxOMQlU7l6328vd_QXOWe8c4WVv2Mh6toJnWXCwIwCghaxMGmqc5qwj96gUlBir-l1CooBPp1Ln-iurmhc1CeySEsCyfS2wa0Xz4AN8VNwMwOHHTJT6fgepWfZIrqby57GsyJ3fuBRekvQIkK_XIQmBYGnwmwGdcBF46j3bSMuAals0PraWUv8NptJaB2U48eGJfbV3H3NnqCniTyhkSuzklrnjjcN8F-Pukus=w530-h375-no',
                alt_text='이미지 오류'
            )
            return [head_section, block1]

    with open(user, "a+") as userfile:
        data = food_name + "/" + str(kal) + "\n"
        userfile.write(data)

    if sumOfcal(user) > getBaseUser(user):
        head_section = SectionBlock(
            text="*" + food_name + "*" + " 을 먹어서 지금 " + "*" + str(
                round(sumOfcal(user) - getBaseUser(user))) + "*" + " 칼로리를 초과했습니다.\n"+uu+" 회원님 갑시다, 진실의 방으로"
        )
        block1 = ImageBlock(
            image_url='https://lh3.googleusercontent.com/zqYPnV3JrUx6Dc4e5XyejXpgToe9AgvLRQS9tZehGM3QJ5bgzn4ecnNbean_vehAc6lanCI_msyG90jiElDMthDEWm1a9ksEPSL9hXGWfvpvB59a_1FvhHV2I3fqgdGpzpeqVOCpdq7Sdgg8sPRR_K3j2Kzwl615_KU88EgQObn_JP_30eMoRXWuqIJOFhlRLyd-nubo9UmnBSWn0t92qu2ZUecdGvpmwqY0sIuOjSo4YORvW-VYYcFureJJRVDpwJh845vWRSPn0rn6amlk61j7Eaevse4X6ML2hJME7yiXxfjfCf1P_ZbxRlJoViPZXJayd_dPmWMTESf6WDDMEo8F4udtzkBo2N1MYgoJdaivWC00wA5zq-tXotVQTkJkZwAjUiDImjlYsCGW39sdZoo9y7uscK1wNcZkYrmnTa0o-LZQ-7r-4d63A67CdSFzPlfKrzkpRqawjCsKwMf_bv7ussAWSz1NhEf36bmHowhCjd14oCpgO4ZHEnGHNG1MOka_0gQIgFD-yw7JVYlLHQ70NsQ9ict5FZL6QNxsn2MkjiODvA6KbZf7zotrKir7tD06Cay5eDF3KbaRs4u1yS9NcR-cr8lCdcS63qnI7UvZNUPFRkkheRtopnBDQKqYnfH_AQbPGgf5qp6Ov5xntkuUOXB5IGE=w480-h347-no',
            alt_text='이미지 오류'
        )
        return [head_section, block1]

    a = round(sumOfcal(user) / getBaseUser(user) * 100)
    if a < 25:
        t ="*" + food_name + "*" + " 의 칼로리는 " + "*" + str(kal) + "*" + " 입니다 "+uu+" 회원님~~.\n" + "누적된 칼로리는 " + str(
            round(sumOfcal(user))) + " / " + str(
            getBaseUser(user)) + " *-------" + str(
            round(sumOfcal(user) / getBaseUser(user) * 100)) + "%" + "*" + " 입니다.\n잘 하고 계시니까, 칼로리 안넘치도록 조심하세요!"
        b = 'https://lh3.googleusercontent.com/CSu1I7gQX8bDjVYVBZxxAjhAVZfg4o2O-rTYXuHvIpwGgfJPV3X5w5iis58nRCQqL16Qubvr1yy2N_YM7ZXGsMhNTKVePFLWNSLG1qOVd7A2D0pd1NVHWW1lUq4BC90_jU9m7F0vw3TpZqONE32IXqwFaEh7X8wPBGBkcfih2yHU0w44FfVnlHhuLhf0jn0qMCpT9TfdfU-FlnymfARPh4BiQP2tTAtA74-JqO_BJwMG-hZJDn0KzFQ2wTO7pxG-D70I2u4SbUHkmsEpD41yxYvdS8pOUpHqlNMuX7CuH3tXS1jWJ-vAZbV27UpfoLBGgEbE3lwA_kaq-iUgQISt7_lrvZcpQ_2byx793fEgWOfCeIPOCr22JkEfXzOeJ_Y4tYOGqUpSLbn5yh8Aj3JmakvtaMtPogfsucrm0cR9kUYW98-n9LstAATvwP4Am44jK0xl8DZ0o8YA5vblX8xX252cQ-uWK0gl4MqNjjlgLbOhaxdExcgQ3e8bGH8TNzh0ewKKjJPI86M5U6fdcxNF4TTzEjC9kH-z-QibqENjaEGzgP3yzuCA7eGAXBPUEqoXAOH3G0KyKPJ0yXUS-IEib8PDI_r5i461spcG83KzRxhpfa5g1EPbUkYWzMEpYBCgYd73UIiwTaXvs9CiIHSKmm7DmkyTvK4=w540-h289-no'
    elif a < 50:
        t ="*" + food_name + "*" + " 의 칼로리는 " + "*" + str(kal) + "*" + " 입니다 "+uu+" 회원님~~.\n" + "누적된 칼로리는 " + str(
            round(sumOfcal(user))) + " / " + str(
            getBaseUser(user)) + " *-------" + str(
            round(sumOfcal(user) / getBaseUser(user) * 100)) + "%" + "*" + " 입니다.\n아오, 회원님 때릴뻔 했네...\n 회원님 적당히 먹으세요\n부탁드리겠습니다~"
        b = 'https://lh3.googleusercontent.com/QG_TduWV3ygep12RCS-h3nuBIJomlBxkTRGxTXXSg9F9PqMCiELoiGbBXzS4V9zQvCDV6hH7Qwy9rJ4VMLFUjLXR0IaPukOzKXisWtu0zdEzsZ9KQfp4TKz2iLHkd8hUKukWHOMhYfd1SukIx-G4pQCBJ8KfWybnr7KB9uXY44kZJOl97aBa3oKyVa3B1ni7zC76f7keWW-ZUH4os1_ZjGRYpd7aTEhEdAH8KI8YvfwEP4uVXMCtEeT_Ruyjd4VXWEDBu4_lg_zz-6e7YSPS7tyOAB_gZ5Oj1jB44X2FOS2fkDx0W_DmwxqA9vBZ-4V1jOPhzdjM0AOMnGfSO-V_dNeHGGrvjHss_BqVnvKrMp_ShgP5IDbxJq5G5VK2qiP4zdB-l4oXwycz1AuhY4_zV_aRRLmPZ7A891Tke2692Dxd2AX5SdoWUWWUZJYGOxFWyCs8E1QvWPr06vyC5MHSr4RZX0bl4ls2l-4I8ncWT-vdD1MfvURs0-miAKMKybhTrSbYXb5qeh8bxbRxab3L_QdNHT57yp20P3SxOh8Pq-OiEJs6jgj1jIWKdPD4_zz7BLXeqowSd3LesCwWRZdLi3442jPOatbKjgJiTk-wnfz87y2fFpX4o7mhn2BTvLUmYyf1wx9ZXEg9uPCS5rVPRBAyt-oYl7U=w674-h448-no'
    elif a < 75:
        t = "*" + food_name + "*" + " 의 칼로리는 " + "*" + str(kal) + "*" + " 입니다 "+uu+" 회원님.\n" + "누적된 칼로리는 " + str(
            round(sumOfcal(user))) + " / " + str(
            getBaseUser(user)) + " *-------" + str(
            round(sumOfcal(user) / getBaseUser(user) * 100)) + "%" + "*" + " 입니다.\n회원님... 상큼하게 터져볼래요?\n지금 칼로리 위험위험 합니다 ^^"
        b = 'https://lh3.googleusercontent.com/WT9FEKwAw66v363gOt5TRBIzhLC_eUUyxgeIUGLRYhiCK_-Igpb0L2Fa2jzdB6fNmt8NftUu2RQ1GZ4B0ZLvNJ5WJSTmYUwgVz-f8AaQrF3Jr3M-Lxiamh1dcluggto_-qtEdSlM_0R4xfK45CpJtk8h-VSW2RNwyLUC4BNpNZsmXoDe14duD_CiODAJOAS0yvCvJQp7yzY2jWy3BUN3QwGxdCmidw9kM2nhzZGKNyo3OCbvBACKGVloxnuCfXQLB96tn4yxBcKjG_gxo0Mxod2kZL4PDWg0ovAEQHkF66mOe7Pyd2xp0wjume36wK4UTXXX2GbGpvZxypkiXm8EFTPDLURVu5Z_XxBCQargbZ9U6tR0c0EBf7SxZw6UAx52IisnVAmDzyvgg-JgLF_YjKb0UsJi2rEvMjMmeJbA9UnG2EWRV90LC3XTDjx34hpK6gPfJSIygx4hxkKZun0_jV0a9bQM-otHiG8_0hElej1wQm0FenEdYBnMBODEDw-48kozRKnUC-wkpqgwOTRN4vxriPkbuM7U1baBji-UZ60LjtVhQS2_ujO0mj-6xKEI5KahZl2Q8TP6MjvlalR3t9PvJKrlp3KRGaT9UWu9JpoWMveBi6nykfi2R6bJJP78BnwOYBjqJpfCgX1i9dJsgetj0ACmaxo=w700-h404-no'
    elif a < 100:
        t = "*" + food_name + "*" + " 의 칼로리는 " + "*" + str(kal) + "*" + " 입니다 "+uu+" 회원님.\n" + "누적된 칼로리는 " + str(
            round(sumOfcal(user))) + " / " + str(
            getBaseUser(user)) + " *-------" + str(
            round(sumOfcal(user) / getBaseUser(user) * 100)) + "%" + "*" + " 입니다.\n회..회원님... \n아 말리지 말아봐요..!!"
        b = 'https://lh3.googleusercontent.com/d-cUNReJdtzfj4Hvy-DEQ1fiIGXgQrtSGOvM1yyuAqq-o3B8iFOJPm40sQjC6qeXyAtkKiTTh6UQKqwVYDp0TfSHUHKDUbnqrUJ-g-zo0y2K-rTLnBV1jcBQTPkj_F0Mo06RBNSfUcgh5A6vfC03vgw1pwIZ2exo_-5YvmHh1BiSFMaB2NLHeBO1RxsfYRj0KayKZIIrojS9osRp6E3A_5QQmjiWcmwp3iqifKV5XLzT6ItJVYFyFgQUVX4yeq3XZUOdOpDa-2g-kzhkQSkFySDK1iv72cCwyFuqn4QxGQFQlFia2rKw26XuNUHQJGJ5kDgU1q-Zg-VUdfrAtwvEOajkw-I_f7cyXos7F2zfTAwK1Ti5QBP1vksU5_5rMeE867DEIG8ybRnMiFJQtdE1oDCkacKzlZM1gt3uspSfkVamKkpzdJ9gF-laaI7d_bE5gsqHe0N5aIvDLlF1WB7no2SA4gQp2HKNPUOCelq__gcEBye1jLgcbcELcGLRxKFzc87zNkOALaqVAJ2HBeR3IfIIzpyKF_ebw_oCpM0F1Rw2ESC4nDkijQbor22FSicbHfeLoRaPTKfwoXk3Et0sHquNyQ_bkBB9aFf5PQQhwhSJkdZLAX5pWPOm3Ou_aWO9ejplSpe82NEbu7CagXGRD-0s9UPhHcI=w550-h367-no'
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
        text="안녕하세요 "+uu+" 회원님~~\n회원님의 식단과 운동을 책임질 마블리입니다\n우선은 회원님의 기본 정보를 입력해볼까요??\n아래 예시 처럼 입력해주세요 회원님~~\n사랑합니다~\n(ex : 남자(성별)/21(나이)/170(키)/60(몸무게))\n도움말 기능은 /help를 입력해주세요~"
    )
    block1 = ImageBlock(
        image_url='https://lh3.googleusercontent.com/j-HyF2P80d2ZHcW9o6S5lY2arkW_jxY3r5rKLrQRRSJQeteRLmcgKu5T2pP5muQxEVVcS4jG-og1yeivxwi26EfjMiTCT-RTcqtSA1U4MwNSM4Bv402JQFrRHZF8t42dEQsioZ0BrNzRa-TQVCMVpgxhLY4e6rOksf_l1XWE393ekpl9Wu1eeO-UdvE-_7MSHvz5zol4lVU-ClMpkuK7wG5LXjQegDwrGu-XlcyYOqYnBIlA0n_2h0A1OR8RKH_pivQKI9dC_BxQ2SAYPcD7Gh2vugsiZZIDZrDy32tzYqunE_ld_LstUM_9gFQ2Ht2IN2fApEqg5N7PK_TZ61lRbL3i_gk81gWqF7kVqJsqslpBQnvWwrJTI5ftDvpMVQHkC8aDRdsJ7e4UoXnyikrsujZZPllRKCrAMEgwjFNJHGAO445EgKQ8IJ7v3x48-E-jql-n3McEV4gmzeh9mGQKVXJe3eCvB7UqlfqIEnDS8DuFN_QD7j6gprDJ6yA_GXM2fvAF4VDNTKCP5tL6h0XObyyt0QwgXLHQgRlRnh1gRxcva8QGZt2VTKsGnGAQC8qFqkwBIIpdFrSG-cz8gJybhxR5Lvchhy0YGqX4-ZZWPCcuyaiYmw-KAkdgBUFTnkTs0ywliOSsCFbceJVMEDdm_vSmKKxXpoU=w400-h283-no',
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
        keywords = "앱 초기 실행은 @Mavely 을 mention\n정보 기입은 성별/나이/키/몸무게  *ex:남자/24/176/65 * 형식으로 기입\n음식 칼로리 검색은 *검색/음식명*\n먹은 음식 계산은 *음식/음식명*\n운동 관련 유튜브 영상 시청은 *운동/?*\n하루 권장 칼로리 안넘기도록 주의하세요!"

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
        keywords = eatFood(food,user_id,uu)
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

import oracledb as cx_Oracle
# Oracle 클라이언트 라이브러리 초기화
cx_Oracle.init_oracle_client(lib_dir="/opt/oracle")
from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from flask_session import Session
from openai import OpenAI
import oracledb
import re
import os
import sys
import urllib.request
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from collections import Counter
from wordcloud import WordCloud
from collections import Counter
import threading
import requests

import time
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

import pickle
import streamlit as st


import datetime
from konlpy.tag import Okt

app = Flask(__name__)
# CORS(app)
USER_SIGN = False
USER_ID = ''








CORS(app, supports_credentials=True)


# 세션 설정
app.config['SECRET_KEY'] = 'codelab1234'  # 보안을 위한 시크릿 키 설정, 실제 시크릿 키는 추측이 불가능하게 보안강도를 높여서 생성한다.
app.config['SESSION_TYPE'] = 'filesystem'  # 세션 데이터를 파일 시스템에 저장
Session(app)

# OpenAI API key 설정

OPEN_API_KEY=
ASSISTANT_ID =
client = OpenAI(api_key=OPEN_API_KEY)
# conn = cx_Oracle.connect('bae/1111@192.168.0.21:1521/xe')
conn = cx_Oracle.connect('garage/1111@localhost:1521/xe')

def infinite_loop():
    while True:
        global USER_SIGN
        global USER_ID
        time.sleep(1)
        print("자 얼마나 나오려나")
        if USER_SIGN:
            try:

                connection = conn
                cursor = connection.cursor()
                cursor.execute("SELECT id,tagfamily,taglike FROM users WHERE id==:id",
                               {'id': USER_ID})

                FASTIVALS = []
                row = cursor.fetchone()

                pattern = r'\b(2024|제\d+회|2023|2025)\b'

                while row:
                    fastival = {
                        'ID': row[0],
                        'TAGFAMILY': re.sub(pattern, '', row[1].replace('#', '').replace(',', ' ')),
                        'TAGLIKE': re.sub(pattern, '', row[2].replace('#', '').replace(',', ' '))
                    }
                    FASTIVALS.append(fastival)
                    row = cursor.fetchone()

                cursor.close()
                print(FASTIVALS)
                print(len(FASTIVALS))

                client_id = "eeUxN1m6ybL7ko87qy3_"
                client_secret = "Gc4VxyIGUM"

                start = 1
                display = 10
                options = Options()
                # options.add_experimental_option("detach", True)
                options.add_argument('--headless')
                service = Service(ChromeDriverManager().install())

                encText = urllib.parse.quote('축제' + FASTIVALS['TAGFAMILY'])

                url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&start=" + str(
                    start) + "&display=" + str(
                    display)  # JSON 결과
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request)
                rescode = response.getcode()
                if (rescode == 200):
                    response_body = response.read()
                else:
                    print("Error Code:" + rescode)

                response_body_str = response_body.decode('utf-8')
                response_json = json.loads(response_body_str)
                links = [result["link"] for result in response_json["items"]]
                filtered_links = [link for link in links if link.startswith("https://blog")]

                list_results = []
                driver = webdriver.Chrome(service=service, options=options)
                for url in filtered_links:

                    driver.get(url)

                    driver.switch_to.default_content()  # frame 초기화
                    driver.switch_to.frame('mainFrame')

                    # switch_frame('mainFrame')
                    html_doc = driver.page_source

                    soup = BeautifulSoup(html_doc, 'html.parser')
                    div_tag = soup.find('div', class_='se-main-container')
                    if div_tag:
                        span_tags = div_tag.find_all('span')
                        texts = [tag.get_text(strip=True) for tag in span_tags]
                    else:
                        print(f"URL: {url} 에서 se-main-container 클래스를 가진 div 태그를 찾을 수 없습니다.")

                    clean_texts1 = [re.sub('<[^<]+?>', '', text) for text in texts]
                    clean_texts = [re.sub('[a-zA-Z0-9]', '', text) for text in clean_texts1]
                    # 결과 출력 및 저장
                    for clean_text in clean_texts:
                        list_results.append(clean_text)
                list_output_filename = "all_results.txt"
                with open(list_output_filename, 'w', encoding='utf-8') as list_output_file:
                    for item in list_results:
                        list_output_file.write("%s\n" % item)

                driver.quit()

                f = open("all_results.txt", 'r', encoding='utf-8')
                lines = f.readlines()
                f.close()

                okt = Okt()
                # temp = []
                # for line in lines:
                #     temp.append(okt.nouns(line))
                # # temp

                word_counter = Counter()
                for line in lines:
                    nouns = okt.nouns(line)
                    word_counter.update(nouns)

                # 가장 많이 등장한 단어 10개 선택
                top_keywords = word_counter.most_common(100)

                def flatten(l):
                    flatList = []
                    for elem in l:
                        if type(elem) == list:
                            for e in elem:
                                flatList.append(e)
                        else:
                            flatList.append(elem)
                    return flatList

                word_list = flatten(top_keywords)

                filtered_keywords = [(word, count) for word, count in top_keywords if len(word) >= 2]
                series_filtered_keywords = pd.Series(dict(filtered_keywords))
                series_filtered_keywords.head(50)

                filtered_keywords_ = {word: freq for word, freq in series_filtered_keywords.items() if
                                      not re.match(r'^축제|축제$', word)}
                exclude_patterns = r'^(지역|가족|어린이|아이들|연인|아내|부부|[ㄱ-ㅎㅏ-ㅣa-zA-Z]+|[^\w]*축제[^\w]*)$'

                filtered_word_counter = Counter()
                for word, freq in filtered_keywords_.items():
                    if not re.match(exclude_patterns, word):
                        filtered_word_counter[word] = freq
                filtered_words1 = {word: count for word, count in filtered_word_counter.items() if count >= 10}
                top_50_words = dict(filtered_word_counter.most_common(50))
                word_list = list(filtered_words1.keys())

                try:
                    connection = conn;
                    cursor = connection.cursor()
                    blog_description = ','.join(word_list)
                    user_like = ','.join(FASTIVALS['TAGLIKE'].split())
                    cursor.execute("insert into user_descrip (id, blog_des) values (:id, :word_list)",
                                   {'id': FASTIVALS['ID'], 'word_list': blog_description + user_like})
                    connection.commit()
                    cursor.close()
                    USER_SIGN = False
                    USER_ID = ''
                except Exception as e:
                    print({'error': str(e)})
                print(word_list)

            except Exception as e:
                print({'error': str(e)})

        else :
            continue
t = threading.Thread(target=infinite_loop, daemon=True)
t.start()

@app.route('/')
@cross_origin(supports_credentials=True)
def index():
    print("::::::응답")
    return "쇼핑몰 데이터 응답 서버에 접속하셨습니다."
@app.route('/ere', methods=['POST'])
@cross_origin(supports_credentials=True)
def solve_equation():
    print("request ok")
    content = request.json['content']
    print(content)

    #
    # # 쓰레드 ID가 세션에 없으면 새로운 쓰레드 생성
    if 'thread_id' not in session:
        thread = client.beta.threads.create()
        session['thread_id'] = thread.id
    #
    try:
    #     # 사용자 메시지를 처리하는 메시지 생성
        message = client.beta.threads.messages.create(
            thread_id=session['thread_id'],
            role="user",
            content=content
        )
    #     # 결과를 받기 위해 실행
        run = client.beta.threads.runs.create_and_poll(
            thread_id=session['thread_id'],
            assistant_id=ASSISTANT_ID,
        )
    #
        if run.status == 'completed':
            # 모든 메시지를 가져오고 마지막 메시지의 내용을 반환
            messages = client.beta.threads.messages.list(thread_id=session['thread_id'])
            last_message = next((m for m in reversed(messages.data) if m.role == 'assistant'), None)
            if last_message:
                return jsonify({"status": "success", "answer": last_message.content[0].text.value})
            else:
                return jsonify({"status": "error", "message": "No response from assistant"})
        else:
            return jsonify({"status": "error", "message": "Failed to complete the run"})

    #
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/usercosineupdate', methods=['POST'])
@cross_origin(supports_credentials=True)
def usercosineupdate():
    global USER_SIGN
    global USER_ID
    data= request.get_json()
    if data is None:
        return jsonify({"result": False, "message": "No data provided"}), 400
    user_id = data.get('id')
    print(user_id +"::::::::::::::::")
    USER_SIGN = True
    USER_ID = user_id

    return jsonify({"result": True}), 200




@app.route('/recommendation', methods=['GET'])
@cross_origin(supports_credentials=True)
def recommendation():
    try:

        user_id = request.args.get('user_id')
        print(user_id)
        # user_id = 'admin'
        conn = cx_Oracle.connect('bae/1111@192.168.0.21:1521/xe')
        connection = conn

        festival_file_load = pickle.load(open('festival.pickle', 'rb'))
        cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))
        festival_file_load['FESTIVALID'] = festival_file_load['FESTIVALID'].astype(int)

        cursor = connection.cursor()
        cursor.execute("SELECT * from user_descrip where id=(:user_id)", {'user_id': user_id})
        row = cursor.fetchone()
        user_descrip = {'FESTIVALID': row[0], 'FESTIVALNAME': row[0], 'BLOG_DES': row[1]}
        new_festival_df = pd.DataFrame([user_descrip])
        new_festival_df['BLOG_DES'].fillna('', inplace=True)
        new_festival_df['BLOG_DES'] = new_festival_df['BLOG_DES'].str.replace(',', ' ')
        festival_file_load = pd.concat([festival_file_load, new_festival_df], ignore_index=True)

        count = CountVectorizer()

        count_matrix = count.fit_transform(festival_file_load['BLOG_DES'])

        cosine_sim = cosine_similarity(count_matrix, count_matrix)

        # idx = festival_file_load[festival_file_load['FESTIVALID'] == user_descrip['FESTIVALID']].index[0]
        idx=(len(festival_file_load)-1)

        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]

        festival_indices = [i[0] for i in sim_scores]

        result = festival_file_load['FESTIVALID'].iloc[festival_indices].tolist()

        cursor = connection.cursor()
        cursor.execute("SELECT f.*, COALESCE(i.image_name, ',') as image_name from festivals f left join festival_image i ON f.festivalid = i.festivalid where f.festivalid in ({})".format(
            ','.join([':{}'.format(i + 1) for i in range(len(result))])),
            result)
        row = cursor.fetchone()
        FASTIVALS = []
        while row:
            fastival = {
                'FESTIVALID': row[0],
                'FESTIVALNAME': row[1],
                'LOCATION': row[2],
                'STARTDATE': row[3].strftime('%Y-%m-%d') if row[3] else None,
                'ENDDATE': row[4].strftime('%Y-%m-%d') if row[4] else None,
                'DESCRIPTION': row[5],  # .read() if row[5] else None,  # LOB 객체 읽기
                'WEBSITE': row[6],
                'ROADADDRESS': row[7],
                'JIBUNADDRESS': row[8],
                'LATITUDE': row[9],
                'LONGITUDE': row[10],
                'IMAGE_NAME': row[11]

            }
            FASTIVALS.append(fastival)
            row = cursor.fetchone()

        cursor.close()
        connection.close()


        return FASTIVALS
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal Server Error'})



if __name__ == '__main__':
    app.run(debug=True)

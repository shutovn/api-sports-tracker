#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request
import requests
import re
import fake_useragent
from bs4 import BeautifulSoup
import json
import datetime
from flaskext.mysql import MySQL
import os

# Получение значенией переменных из docker-compose environment
md_user = os.environ['DB_USER']
md_pass = os.environ['DB_PASSWORD']
md_base = os.environ['DB_DATABASE']
md_host = os.environ['DB_HOST']
login_st = os.environ['ST_LOGIN']
password_st = os.environ['ST_PASS']
token_st = os.environ['ST_TOKEN']

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = md_user
app.config['MYSQL_DATABASE_PASSWORD'] = md_pass
app.config['MYSQL_DATABASE_DB'] = md_base
app.config['MYSQL_DATABASE_HOST'] = md_host
mysql.init_app(app)

# Тест общей функции для всех routers
def time():
    now = datetime.datetime.now()
    return str(now)

#Begin Переменные для подключения к сервису sports-tracker.com
header = {
    'User-Agent': 'user' ,
    'STTAuthorization':	f'{token_st}'
}

data = {
    "l": f"{login_st}" ,
    "p": f"{password_st}"
}
#End Конец Переменные для подключения к сервису sports-tracker.com

@app.route('/hello')
def hello_world():
    return f"Здравствуйте! Flask - работает.  Текущая дата: {time()}"


@app.route("/test_mysql")
def test_mysql():
    conn = mysql.connect()
    cursor =conn.cursor()

    sql_query = "SELECT * FROM workout.workouts;"
    cursor.execute(sql_query)
    data = cursor.fetchall()

    #sql_query = "SELECT workoutkey FROM workout.workouts WHERE workoutkey = '<key_workout>';"
    #cursor.execute(sql_query)
    #data = cursor.fetchone()

    #if data == None:
    #    data = "Нет такого ключа и надо записать!"
    #else:
    #    data = "Такой ключ уже есть и не надо записывать!"
    cursor.close()

    return jsonify(data)
    #return str(data)


@app.route("/workouts_json")
def workouts_json():
    amount = request.args.get('amount')
    if amount == None:
        amount = 10

    workout_dict = {}

    session = requests.Session()
    link = "https://api.sports-tracker.com/apiserver/v1/login"
    user = fake_useragent.UserAgent().random

    session.post(link, data=data, headers=header)

    # Получить последние x тренировок
    workout_info = f"https://api.sports-tracker.com/apiserver/v1/workouts?sortonst=true&limit={amount}&offset=0"

    # Получить список картинок тренировки, но без url
    # workout_info = f"https://api.sports-tracker.com/apiserver/v1/images/workout/<key_workout>"

    # Получить ВСЮ информацию по тренировке
    # workout_info = f"https://api.sports-tracker.com/apiserver/v1/workouts/<key_workout>"

    # Получить ВСЮ информацию по тренировке
    # workout_info = f"https://api.sports-tracker.com/apiserver/v1/workouts/<key_workout>/data"

    workout_responce = session.get(workout_info, headers=header)

    workout = workout_responce.json()

    return jsonify(workout)

# Запись последних тренировок в БД, новых стренировок которые еще не записаны в БД. кол-во должно передаваться аргументом к запросу.
@app.route("/workout_last")
def workout():
    amount = request.args.get('amount')
    if amount == None:
        amount = 30

    workout_dict = {}

    session = requests.Session()
    link = "https://api.sports-tracker.com/apiserver/v1/login"
    user = fake_useragent.UserAgent().random

    session.post(link, data=data, headers=header)

    workout_info = f"https://api.sports-tracker.com/apiserver/v1/workouts?sortonst=true&limit={amount}&offset=0"
    workout_responce = session.get(workout_info, headers=header)

    workout = workout_responce.json()

    list_var = ('workoutKey', 'startTime', 'stopTime', 'activityId', 'totalTime', 'totalDistance', 'avgSpeed', 'workoutName', 'recoveryTime', 'energyConsumption', 'description')
    list_tmp = {}
    flag = 0
    c = 0

    # Откпываем соединение с БД
    conn = mysql.connect()
    cursor =conn.cursor()

    while True and flag == 0 and amount != c:
        for i in list_var:
            var = i
            try:
                try:
                    i = workout['payload'][c][i]
                except IndexError:
                    break
            except KeyError:
                if i == "workoutName":
                    try:
                        i = workout['payload'][c]['description']
                    except KeyError:
                        i = "Без названия!"
                if i == "description":
                    try:
                        i = workout['payload'][c]['workoutName']
                    except KeyError:
                        i = "Без названия!"
            list_tmp[var] = i

        workout_dict[c] = dict(list_tmp)

        startTime = workout_dict[c]['startTime']
        stopTime = workout_dict[c]['stopTime']
        activityId = workout_dict[c]['activityId']
        totalTime = workout_dict[c]['totalTime']
        totalDistance = workout_dict[c]['totalDistance']
        avgSpeed = workout_dict[c]['avgSpeed']
        workoutKey = workout_dict[c]['workoutKey']
        workoutName = workout_dict[c]['workoutName']
        recoveryTime = workout_dict[c]['recoveryTime']
        energyConsumption = workout_dict[c]['energyConsumption']
        description = workout_dict[c]['description']

        sql_query = f"SELECT workoutkey FROM workout.workouts WHERE workoutkey = '{workoutKey}';"
        cursor.execute(sql_query)
        sql_data = cursor.fetchone()

        if sql_data == None:
            timestamp = str(time())
            sql = f"""
            INSERT INTO `workout`.`workouts` (
            `date_create`,
            `name`,
            `starttime`,
            `stoptime`,
            `totaltime`,
            `activityid`,
            `totaldistance`,
            `avgspeed`,
            `workoutkey`,
            `recoverytime`,
            `energy`,
            `description`)
            VALUES (
            '{timestamp}',
            '{workoutName}',
            '{startTime}',
            '{stopTime}',
            '{totalTime}',
            '{activityId}',
            '{totalDistance}',
            '{avgSpeed}',
            '{workoutKey}',
            '{recoveryTime}',
            '{energyConsumption}',
            '{description}'
            );
            """
            cursor.execute(sql)
            conn.commit()
        else:
            flag = 1
        c += 1

    cursor.close()

    return dict(workout_dict)

    # Пример вывода данных в формате JSON
    #return jsonify(totalTime)
    #return jsonify(workout)


@app.route("/export_workout")
def export_workout():

    url = "https://api.sports-tracker.com/apiserver/v1/workout/exportGpx/"
    count = 0

    conn = mysql.connect()
    cursor =conn.cursor()

    sql_query = "SELECT workoutkey,id_workout FROM workout.workouts WHERE export = 0;"
    cursor.execute(sql_query)
    data = cursor.fetchall()

    for i in data:
        key = i[0]
        id = i[1]
        # Скачивание и запись gpx файлов тренировок
        workout_url_gpx = f"{url}{key}?token={token_st}"
        r = requests.get(workout_url_gpx)
        content_disposition = r.headers['Content-Disposition']
        file_name = re.findall('filename="(.+)"', content_disposition)[0]
        open(f"treks/{key}.gpx", 'wb').write(r.content)
        path_to_gpx = f"treks/{key}.gpx"
        # Счетчик записанных файлов
        count += 1

        test_id = f"SELECT id_gpx FROM `workout`.`workouts_gpx` WHERE `id_workout` = '{id}';"
        cursor.execute(test_id)
        sql_data = cursor.fetchone()

        if sql_data == None:
            # Запись файла в БД
            timestamp = str(time())

            query_insert_export = f"""
            INSERT INTO `workout`.`workouts_gpx` (
            `date_create`,
            `id_workout`,
            `path_gpx`)
            VALUES (
            '{timestamp}',
            '{id}',
            '{path_to_gpx}'
            );
            """
            cursor.execute(query_insert_export)
            conn.commit()

            query_set_export = f"""
            UPDATE `workout`.`workouts`
            SET `export` = '1'
            WHERE (`id_workout` = '{id}'
            );
            """
            cursor.execute(query_set_export)
            conn.commit()

    cursor.close()
    trek = count

    return str(trek)


@app.route("/update_workout_description")
def update_workout_description():
    url = "https://api.sports-tracker.com/apiserver/v1/workouts/similarRoutes/"
    count = 0

    # Получение всех id тренировок
    conn = mysql.connect()
    cursor =conn.cursor()

    sql_query = "SELECT workoutkey FROM workout.workouts;"
    cursor.execute(sql_query)
    data_sql = cursor.fetchall()

    # Открытие ссесии авторизации
    session = requests.Session()
    link = "https://api.sports-tracker.com/apiserver/v1/login"
    user = fake_useragent.UserAgent().random
    responce = session.post(link, data=data, headers=header)

    # Прогон по ключу всех тренировок имеющихся в локальной БД
    for id in data_sql:
        key = id[0]
        workout_info = f"{url}{key}"
        workout_responce = session.get(workout_info, headers=header)
        workout = workout_responce.json()
        try:
            valuedescription = workout['payload'][0]['description']
        except KeyError:
            valuedescription = "Нет описания!"
        except IndexError:
            valuedescription = f"Тренировка {key} имеет пустой payload."

        # Взятие значения из локальной БД
        sql_query_description = f"SELECT description FROM `workout`.`workouts` WHERE `workoutkey` = '{key}';"
        cursor.execute(sql_query_description)
        data_sql_description = cursor.fetchone()

        # Запись в локальную БД
        if valuedescription != "" and str(data_sql_description[0]) != str(valuedescription):
            timestamp = str(time())
            query_update_description = f"""
            UPDATE `workout`.`workouts`
            SET `date_update` = '{timestamp}',
            `description` = '{valuedescription}'
            WHERE (`workoutkey` = '{key}'
            );
            """
            cursor.execute(query_update_description)
            conn.commit()
            count += 1

    # Закрытие подключения к БД
    conn = mysql.connect()
    cursor =conn.cursor()

    return str("UPDATE ")+str(count)+str(" rows.")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

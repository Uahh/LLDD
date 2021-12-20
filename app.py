# -*- coding: utf-8 -*-
import os
import json
import random
from re import A
# from models import functions
from flask import Flask, request, url_for, redirect
from flask import render_template
import config

app = Flask(__name__, template_folder='templates', static_folder='static')
print('Waiting......')


def get_all_pic(idol):
    main_num = random.randint(1, 5)
    other_num = 9 - main_num
    dir_list = os.listdir(config.pic_dir)
    dir_list.remove(idol)
    main_idol_path = get_idol_pic(idol, main_num)

    other_idol_path = []
    for i in range(0, other_num):
        random_idol = random.randint(0, len(dir_list) - 1)
        random_idol_pic = get_idol_pic(dir_list[random_idol], 1)
        other_idol_path.append(random_idol_pic[0])
    
    result = main_idol_path + other_idol_path
    random.shuffle(result)
    ans_array = []
    for i in range(0, len(result)):
        if idol in result[i]:
            ans_array.append(i + 1)
    return result, ans_array


def get_idol_pic(idol, num):
    res = []
    file_names_list = os.listdir('static/' + config.idol_json[idol]['picture'])
    for i in range(0, num):
        random_file = random.randint(0, len(file_names_list) - 1)
        file = config.idol_json[idol]['picture'] + '/' + file_names_list[random_file]
        res.append(file)
        # res.append(os.path.join(os.getcwd(), file))
        del file_names_list[random_file]
    return res

# 主要逻辑视图函数

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    return render_template('beginning.html')


@app.route('/mid', methods=["GET", "POST"])
def mid():
    json_data = request.get_data(as_text=True)
    json_data = json.loads(json_data)
    if len(json_data['select_idols']) != 0:
        first = json_data['select_idols'][0]
        del json_data['select_idols'][0]
    else:
        return
    if first in config.idol_json.keys():
        json_data['file_list'], json_data['ans_num'] = get_all_pic(first)
    
    return render_template(
        'middle.html',
        idol=first,
        p1=json_data['file_list'][0],
        p2=json_data['file_list'][1],
        p3=json_data['file_list'][2],
        p4=json_data['file_list'][3],
        p5=json_data['file_list'][4],
        p6=json_data['file_list'][5],
        p7=json_data['file_list'][6],
        p8=json_data['file_list'][7],
        p9=json_data['file_list'][8],
        ans=json_data['ans_num'],
        idol_list=json_data['select_idols'],
        user_id=json_data['user_id']
    )


@app.route('/data', methods=["POST"])
def data():
    json_data = request.get_data(as_text=True)
    json_data = json.loads(json_data)
    for idol in json_data['select_idols']:
        if idol in config.idol_json.keys():
            json_data['file_list'] = get_all_pic(idol)

    return json_data


@app.route('/error')
def error():
    return '404 not found'


app.run(host='0.0.0.0', debug=True, port=173)  # inami

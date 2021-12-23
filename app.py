# -*- coding: utf-8 -*-
import os
import json
import copy
import random
from re import A, template
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
        file = config.idol_json[idol]['picture'] + \
            '/' + file_names_list[random_file]
        res.append(file)
        # res.append(os.path.join(os.getcwd(), file))
        del file_names_list[random_file]
    return res


def create_value(value, name):
    ans = "{ value: V, name: \"N\" },"
    return ans.replace('V', str(value)).replace('N', name)

# 主要逻辑视图函数


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    return render_template('beginning.html')


@app.route('/mid', methods=["GET", "POST"])
def mid():
    json_data = request.get_data(as_text=True)
    json_data = json.loads(json_data)
    percent = int(100 / (len(json_data['back_up']) * 3))

    if len(json_data['select_idols']) != 0:
        first = json_data['select_idols'][0]
        del json_data['select_idols'][0]
    elif len(json_data['questions']) != 0:
        # 提问
        first = json_data['questions'][0]
        question = config.idol_json[first]['questions']
        if json_data['question_index'] % 2 == 0:
            del json_data['questions'][0]
            topic = question[1]['topic']
            a = question[1]['a']
            b = question[1]['b']
            c = question[1]['c']
            d = question[1]['d']
            answer = question[1]['answer']
        else:
            topic = question[0]['topic']
            a = question[0]['a']
            b = question[0]['b']
            c = question[0]['c']
            d = question[0]['d']
            answer = question[0]['answer']
        return render_template(
            "test.html",
            color=config.idol_json[first]['color'],
            topic=topic,
            A=a,
            B=b,
            C=c,
            D=d,
            ans=answer,
            user_id=json_data['user_id'],
            percent=json_data['percent'] + float(percent),
            back_up_py=json_data['back_up'],
            questions_py=json_data['questions'],
            point_py=json_data['point'],
            question_index=json_data['question_index']
        )
    else:
        # 总结
        Point = config.Point()
        idol_length = len(json_data['back_up'])

        first_half = 0
        for i in range(0, idol_length):
            first_half += float(json_data['point'][i])
        first_half = 60 * (first_half / idol_length)

        second_half = 0
        for i in range(idol_length, idol_length * 3):
            second_half += float(json_data['point'][i])
        second_half = 40 * (second_half / (idol_length * 2))
        total_point = first_half + second_half

        temp_list = []
        for i in range(idol_length, idol_length * 3, 2):
            temp_list.append(float(json_data['point'][i]) + float(json_data['point'][i + 1]))
        
        idol_point = [0] * idol_length
        idol_total_point = 0
        for i in range(0, idol_length):
            idol_point[i] = (float(json_data['point'][i]) + temp_list[i])
            idol_total_point += idol_point[i]
        
        cnt = 0
        for idol in json_data['back_up']:
            # { value: 1048, name: 'Baidu' },
            Point.idol_dic[idol] = create_value((idol_point[cnt] / idol_total_point) * 100, config.idol_json[idol]['name'])
            Point.idol_color_dic[idol + '_c'] = "\"" + \
                (config.idol_json[idol]['color']) + "\","
            cnt += 1

            cur_group = config.idol_json[idol]['group'][1]
            Point.idol_group_point[cur_group] += 1
            Point.idol_group[cur_group] = create_value(Point.idol_group_point[cur_group], cur_group)
            Point.idol_color_group[cur_group + '_c'] = "\"" + \
                (config.group_json[cur_group]['color']) + "\","
        return render_template(
            'ending.html',
            total_point=total_point,
            Ms=Point.idol_group["μ's"],
            Aq=Point.idol_group["Aqours"],
            Ms_c=Point.idol_color_group["μ's_c"],
            Aq_c=Point.idol_color_group["Aqours_c"],

            Aida_Rikako=Point.idol_dic["Aida_Rikako"],
            Furihata_Ai=Point.idol_dic["Furihata_Ai"],
            Iida_Riho=Point.idol_dic["Iida_Riho"],
            Inami_Anju=Point.idol_dic["Inami_Anju"],
            Kobayashi_Aika=Point.idol_dic["Kobayashi_Aika"],
            Komiya_Arisa=Point.idol_dic["Komiya_Arisa"],
            Kubo_Yurika=Point.idol_dic["Kubo_Yurika"],
            Kusuda_Aina=Point.idol_dic["Kusuda_Aina"],
            Mimori_Suzuko=Point.idol_dic["Mimori_Suzuko"],
            Nanjo_Yoshino=Point.idol_dic["Nanjo_Yoshino"],
            Nitta_Emi=Point.idol_dic["Nitta_Emi"],
            Pile=Point.idol_dic["Pile"],
            Saito_Shuka=Point.idol_dic["Saito_Shuka"],
            Suwa_Nanaka=Point.idol_dic["Suwa_Nanaka"],
            Suzuki_Aina=Point.idol_dic["Suzuki_Aina"],
            Takatsuki_Kanako=Point.idol_dic["Takatsuki_Kanako"],
            Tokui_Sora=Point.idol_dic["Tokui_Sora"],
            Uchida_Aya=Point.idol_dic["Uchida_Aya"],

            Aida_Rikako_c=Point.idol_color_dic["Aida_Rikako_c"],
            Furihata_Ai_c=Point.idol_color_dic["Furihata_Ai_c"],
            Iida_Riho_c=Point.idol_color_dic["Iida_Riho_c"],
            Inami_Anju_c=Point.idol_color_dic["Inami_Anju_c"],
            Kobayashi_Aika_c=Point.idol_color_dic["Kobayashi_Aika_c"],
            Komiya_Arisa_c=Point.idol_color_dic["Komiya_Arisa_c"],
            Kubo_Yurika_c=Point.idol_color_dic["Kubo_Yurika_c"],
            Kusuda_Aina_c=Point.idol_color_dic["Kusuda_Aina_c"],
            Mimori_Suzuko_c=Point.idol_color_dic["Mimori_Suzuko_c"],
            Nanjo_Yoshino_c=Point.idol_color_dic["Nanjo_Yoshino_c"],
            Nitta_Emi_c=Point.idol_color_dic["Nitta_Emi_c"],
            Pile_c=Point.idol_color_dic["Pile_c"],
            Saito_Shuka_c=Point.idol_color_dic["Saito_Shuka_c"],
            Suwa_Nanaka_c=Point.idol_color_dic["Suwa_Nanaka_c"],
            Suzuki_Aina_c=Point.idol_color_dic["Suzuki_Aina_c"],
            Takatsuki_Kanako_c=Point.idol_color_dic["Takatsuki_Kanako_c"],
            Tokui_Sora_c=Point.idol_color_dic["Tokui_Sora_c"],
            Uchida_Aya_c=Point.idol_color_dic["Uchida_Aya_c"]
        )

    # 图片
    if first in config.idol_json.keys():
        json_data['file_list'], json_data['ans_num'] = get_all_pic(first)

    if 'percent' in json_data.keys():
        json_data['percent'] += float(percent)
    else: 
        # 代表第一次进入
        json_data['percent'] = 0
        json_data['point'] = []
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
        idol_list_py=json_data['select_idols'],
        back_up_py=json_data['back_up'],
        questions_py=json_data['questions'],
        user_id=json_data['user_id'],
        percent=json_data['percent'],
        point_py=json_data['point']
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


app.run(host='0.0.0.0', debug=False, port=17173)  # inami

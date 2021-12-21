# -*- coding: utf-8 -*-
import os
import json
import copy
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

def create_value(value, name):
    ans = "{ value: V, name: \"N\" },"
    return ans.replace('V', str(value)).replace('N', name)

# 主要逻辑视图函数

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    return render_template('beginning.html')
    # a = "{ value: 679, name: \"μ\'s\", selected: true }"
    # b = "{ value: 679, name: \"Aqours\" }"
    # c = "\"#000000\""
    # d = ""
    # e = "{ value: 1048, name: \"Nitta Emi\" }"
    # return render_template(
    #     'ending.html', 
    #     Ms=a,
    #     Aq=b,
    #     MsC=c,
    #     AqC=d,
    #     Nitta_Emi=e
    # )


@app.route('/mid', methods=["GET", "POST"])
def mid():
    json_data = request.get_data(as_text=True)
    json_data = json.loads(json_data)
    if len(json_data['select_idols']) != 0:
        first = json_data['select_idols'][0]
        del json_data['select_idols'][0]
    else:
        point = config.Point()
        for idol in json_data['back_up']:
            # { value: 1048, name: 'Baidu' },
            point.idol_dic[idol] = create_value(1, config.idol_json[idol]['roman'])
            point.idol_color_dic[idol + '_c'] = "\"" + (config.idol_json[idol]['color']) + "\","
        return render_template(
            'ending.html',
            # Ms=a,
            # Aq=b,
            # MsC=c,
            # AqC=d,
            Aida_Rikako=point.idol_dic["Aida_Rikako"],
            Furihata_Ai=point.idol_dic["Furihata_Ai"],
            Iida_Riho=point.idol_dic["Iida_Riho"],
            Inami_Anju=point.idol_dic["Inami_Anju"],
            Kobayashi_Aika=point.idol_dic["Kobayashi_Aika"],
            Komiya_Arisa=point.idol_dic["Komiya_Arisa"],
            Kubo_Yurika=point.idol_dic["Kubo_Yurika"],
            Kusuda_Aina=point.idol_dic["Kusuda_Aina"],
            Mimori_Suzuko=point.idol_dic["Mimori_Suzuko"],
            Nanjo_Yoshino=point.idol_dic["Nanjo_Yoshino"],
            Nitta_Emi=point.idol_dic["Nitta_Emi"],
            Pile=point.idol_dic["Pile"],
            Saito_Shuka=point.idol_dic["Saito_Shuka"],
            Suwa_Nanaka=point.idol_dic["Suwa_Nanaka"],
            Suzuki_Aina=point.idol_dic["Suzuki_Aina"],
            Takatsuki_Kanako=point.idol_dic["Takatsuki_Kanako"],
            Tokui_Sora=point.idol_dic["Tokui_Sora"],
            Uchida_Aya=point.idol_dic["Uchida_Aya"],

            Aida_Rikako_c=point.idol_color_dic["Aida_Rikako_c"],
            Furihata_Ai_c=point.idol_color_dic["Furihata_Ai_c"],
            Iida_Riho_c=point.idol_color_dic["Iida_Riho_c"],
            Inami_Anju_c=point.idol_color_dic["Inami_Anju_c"],
            Kobayashi_Aika_c=point.idol_color_dic["Kobayashi_Aika_c"],
            Komiya_Arisa_c=point.idol_color_dic["Komiya_Arisa_c"],
            Kubo_Yurika_c=point.idol_color_dic["Kubo_Yurika_c"],
            Kusuda_Aina_c=point.idol_color_dic["Kusuda_Aina_c"],
            Mimori_Suzuko_c=point.idol_color_dic["Mimori_Suzuko_c"],
            Nanjo_Yoshino_c=point.idol_color_dic["Nanjo_Yoshino_c"],
            Nitta_Emi_c=point.idol_color_dic["Nitta_Emi_c"],
            Pile_c=point.idol_color_dic["Pile_c"],
            Saito_Shuka_c=point.idol_color_dic["Saito_Shuka_c"],
            Suwa_Nanaka_c=point.idol_color_dic["Suwa_Nanaka_c"],
            Suzuki_Aina_c=point.idol_color_dic["Suzuki_Aina_c"],
            Takatsuki_Kanako_c=point.idol_color_dic["Takatsuki_Kanako_c"],
            Tokui_Sora_c=point.idol_color_dic["Tokui_Sora_c"],
            Uchida_Aya_c=point.idol_color_dic["Uchida_Aya_c"]
        )
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
        idol_list_py=json_data['select_idols'],
        back_up_py=json_data['back_up'],
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

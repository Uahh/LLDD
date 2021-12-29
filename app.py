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


def create_ins(value, name):
    ans = "V% 的 N,"
    return ans.replace('V', str(value)).replace('N', name)


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
            temp_list.append(
                float(json_data['point'][i]) + float(json_data['point'][i + 1]))

        idol_point = [0] * idol_length
        idol_total_point = 0
        for i in range(0, idol_length):
            idol_point[i] = (float(json_data['point'][i]) + temp_list[i])
            idol_total_point += idol_point[i]

        cnt = 0
        for idol in json_data['back_up']:
            # { value: 1048, name: 'Baidu' },
            Point.idol_dic[idol] = create_value(
                (idol_point[cnt] / idol_total_point) * 100, config.idol_json[idol]['name'])
            Point.idol_ins_dic[idol + '_i'] = create_ins(
                (idol_point[cnt] / idol_total_point) * 100, config.idol_json[idol]['name'])
            Point.idol_color_dic[idol + '_c'] = "\"" + \
                (config.idol_json[idol]['color']) + "\","
            Point.idol_color_dic[idol + '_rc'] = config.idol_json[idol]['color']
            cnt += 1

            cur_group = config.idol_json[idol]['group'][1]
            Point.idol_group_point[cur_group] += 1
            Point.idol_group[cur_group] = create_value(
                Point.idol_group_point[cur_group], cur_group)
            Point.idol_color_group[cur_group + '_c'] = "\"" + \
                (config.group_json[cur_group]['color']) + "\","
        return render_template(
            'ending.html',
            user_id=json_data['user_id'],
            total_point=total_point,
            Ms=Point.idol_group["μ's"],
            Aq=Point.idol_group["Aqours"],
            Na=Point.idol_group["Saint Snow"],
            Sa=Point.idol_group["虹ヶ咲学園スクールアイドル同好会"],
            Li=Point.idol_group["Liella"],
            Ms_c=Point.idol_color_group["μ's_c"],
            Aq_c=Point.idol_color_group["Aqours_c"],
            Na_c=Point.idol_color_group["Saint Snow_c"],
            Sa_c=Point.idol_color_group["虹ヶ咲学園スクールアイドル同好会_c"],
            Li_c=Point.idol_color_group["Liella_c"],

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
            Sato_Hinata=Point.idol_dic["Sato_Hinata"],
            Tano_Asami=Point.idol_dic["Tano_Asami"],
            Onishi_Aguri=Point.idol_dic["Onishi_Aguri"],
            Sagara_Mayu=Point.idol_dic["Sagara_Mayu"],
            Maeda_Kaori=Point.idol_dic["Maeda_Kaori"],
            Kubota_Miyu=Point.idol_dic["Kubota_Miyu"],
            Murakami_Natsumi=Point.idol_dic["Murakami_Natsumi"],
            Kito_Akari=Point.idol_dic["Kito_Akari"],
            Kusunoki_Tomori=Point.idol_dic["Kusunoki_Tomori"],
            Sashide_Maria=Point.idol_dic["Sashide_Maria"],
            Tanaka_Chiemi=Point.idol_dic["Tanaka_Chiemi"],
            Koizumi_Moeka=Point.idol_dic["Koizumi_Moeka"],
            Uchida_Shu=Point.idol_dic["Uchida_Shu"],
            Houmoto_Akina=Point.idol_dic["Houmoto_Akina"],
            Yano_Hinaki=Point.idol_dic["Yano_Hinaki"],
            Date_Sayuri=Point.idol_dic["Date_Sayuri"],
            Liyuu=Point.idol_dic["Liyuu"],
            Misaki_Nako=Point.idol_dic["Misaki_Nako"],
            Payton_Naomi=Point.idol_dic["Payton_Naomi"],
            Aoyama_Nagisa=Point.idol_dic["Aoyama_Nagisa"],

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
            Uchida_Aya_c=Point.idol_color_dic["Uchida_Aya_c"],
            Sato_Hinata_c=Point.idol_color_dic["Sato_Hinata_c"],
            Tano_Asami_c=Point.idol_color_dic["Tano_Asami_c"],
            Onishi_Aguri_c=Point.idol_color_dic["Onishi_Aguri_c"],
            Sagara_Mayu_c=Point.idol_color_dic["Sagara_Mayu_c"],
            Maeda_Kaori_c=Point.idol_color_dic["Maeda_Kaori_c"],
            Kubota_Miyu_c=Point.idol_color_dic["Kubota_Miyu_c"],
            Murakami_Natsumi_c=Point.idol_color_dic["Murakami_Natsumi_c"],
            Kito_Akari_c=Point.idol_color_dic["Kito_Akari_c"],
            Kusunoki_Tomori_c=Point.idol_color_dic["Kusunoki_Tomori_c"],
            Sashide_Maria_c=Point.idol_color_dic["Sashide_Maria_c"],
            Tanaka_Chiemi_c=Point.idol_color_dic["Tanaka_Chiemi_c"],
            Koizumi_Moeka_c=Point.idol_color_dic["Koizumi_Moeka_c"],
            Uchida_Shu_c=Point.idol_color_dic["Uchida_Shu_c"],
            Houmoto_Akina_c=Point.idol_color_dic["Houmoto_Akina_c"],
            Yano_Hinaki_c=Point.idol_color_dic["Yano_Hinaki_c"],
            Date_Sayuri_c=Point.idol_color_dic["Date_Sayuri_c"],
            Liyuu_c=Point.idol_color_dic["Liyuu_c"],
            Misaki_Nako_c=Point.idol_color_dic["Misaki_Nako_c"],
            Payton_Naomi_c=Point.idol_color_dic["Payton_Naomi_c"],
            Aoyama_Nagisa_c=Point.idol_color_dic["Aoyama_Nagisa_c"],

            Aida_Rikako_i=Point.idol_ins_dic["Aida_Rikako_i"],
            Furihata_Ai_i=Point.idol_ins_dic["Furihata_Ai_i"],
            Iida_Riho_i=Point.idol_ins_dic["Iida_Riho_i"],
            Inami_Anju_i=Point.idol_ins_dic["Inami_Anju_i"],
            Kobayashi_Aika_i=Point.idol_ins_dic["Kobayashi_Aika_i"],
            Komiya_Arisa_i=Point.idol_ins_dic["Komiya_Arisa_i"],
            Kubo_Yurika_i=Point.idol_ins_dic["Kubo_Yurika_i"],
            Kusuda_Aina_i=Point.idol_ins_dic["Kusuda_Aina_i"],
            Mimori_Suzuko_i=Point.idol_ins_dic["Mimori_Suzuko_i"],
            Nanjo_Yoshino_i=Point.idol_ins_dic["Nanjo_Yoshino_i"],
            Nitta_Emi_i=Point.idol_ins_dic["Nitta_Emi_i"],
            Pile_i=Point.idol_ins_dic["Pile_i"],
            Saito_Shuka_i=Point.idol_ins_dic["Saito_Shuka_i"],
            Suwa_Nanaka_i=Point.idol_ins_dic["Suwa_Nanaka_i"],
            Suzuki_Aina_i=Point.idol_ins_dic["Suzuki_Aina_i"],
            Takatsuki_Kanako_i=Point.idol_ins_dic["Takatsuki_Kanako_i"],
            Tokui_Sora_i=Point.idol_ins_dic["Tokui_Sora_i"],
            Uchida_Aya_i=Point.idol_ins_dic["Uchida_Aya_i"],
            Sato_Hinata_i=Point.idol_ins_dic["Sato_Hinata_i"],
            Tano_Asami_i=Point.idol_ins_dic["Tano_Asami_i"],
            Onishi_Aguri_i=Point.idol_ins_dic["Onishi_Aguri_i"],
            Sagara_Mayu_i=Point.idol_ins_dic["Sagara_Mayu_i"],
            Maeda_Kaori_i=Point.idol_ins_dic["Maeda_Kaori_i"],
            Kubota_Miyu_i=Point.idol_ins_dic["Kubota_Miyu_i"],
            Murakami_Natsumi_i=Point.idol_ins_dic["Murakami_Natsumi_i"],
            Kito_Akari_i=Point.idol_ins_dic["Kito_Akari_i"],
            Kusunoki_Tomori_i=Point.idol_ins_dic["Kusunoki_Tomori_i"],
            Sashide_Maria_i=Point.idol_ins_dic["Sashide_Maria_i"],
            Tanaka_Chiemi_i=Point.idol_ins_dic["Tanaka_Chiemi_i"],
            Koizumi_Moeka_i=Point.idol_ins_dic["Koizumi_Moeka_i"],
            Uchida_Shu_i=Point.idol_ins_dic["Uchida_Shu_i"],
            Houmoto_Akina_i=Point.idol_ins_dic["Houmoto_Akina_i"],
            Yano_Hinaki_i=Point.idol_ins_dic["Yano_Hinaki_i"],
            Date_Sayuri_i=Point.idol_ins_dic["Date_Sayuri_i"],
            Liyuu_i=Point.idol_ins_dic["Liyuu_i"],
            Misaki_Nako_i=Point.idol_ins_dic["Misaki_Nako_i"],
            Payton_Naomi_i=Point.idol_ins_dic["Payton_Naomi_i"],
            Aoyama_Nagisa_i=Point.idol_ins_dic["Aoyama_Nagisa_i"],

            Aida_Rikako_rc=Point.idol_color_dic["Aida_Rikako_rc"],
            Furihata_Ai_rc=Point.idol_color_dic["Furihata_Ai_rc"],
            Iida_Riho_rc=Point.idol_color_dic["Iida_Riho_rc"],
            Inami_Anju_rc=Point.idol_color_dic["Inami_Anju_rc"],
            Kobayashi_Aika_rc=Point.idol_color_dic["Kobayashi_Aika_rc"],
            Komiya_Arisa_rc=Point.idol_color_dic["Komiya_Arisa_rc"],
            Kubo_Yurika_rc=Point.idol_color_dic["Kubo_Yurika_rc"],
            Kusuda_Aina_rc=Point.idol_color_dic["Kusuda_Aina_rc"],
            Mimori_Suzuko_rc=Point.idol_color_dic["Mimori_Suzuko_rc"],
            Nanjo_Yoshino_rc=Point.idol_color_dic["Nanjo_Yoshino_rc"],
            Nitta_Emi_rc=Point.idol_color_dic["Nitta_Emi_rc"],
            Pile_rc=Point.idol_color_dic["Pile_rc"],
            Saito_Shuka_rc=Point.idol_color_dic["Saito_Shuka_rc"],
            Suwa_Nanaka_rc=Point.idol_color_dic["Suwa_Nanaka_rc"],
            Suzuki_Aina_rc=Point.idol_color_dic["Suzuki_Aina_rc"],
            Takatsuki_Kanako_rc=Point.idol_color_dic["Takatsuki_Kanako_rc"],
            Tokui_Sora_rc=Point.idol_color_dic["Tokui_Sora_rc"],
            Uchida_Aya_rc=Point.idol_color_dic["Uchida_Aya_rc"],
            Sato_Hinata_rc=Point.idol_color_dic["Sato_Hinata_rc"],
            Tano_Asami_rc=Point.idol_color_dic["Tano_Asami_rc"],
            Onishi_Aguri_rc=Point.idol_color_dic["Onishi_Aguri_rc"],
            Sagara_Mayu_rc=Point.idol_color_dic["Sagara_Mayu_rc"],
            Maeda_Kaori_rc=Point.idol_color_dic["Maeda_Kaori_rc"],
            Kubota_Miyu_rc=Point.idol_color_dic["Kubota_Miyu_rc"],
            Murakami_Natsumi_rc=Point.idol_color_dic["Murakami_Natsumi_rc"],
            Kito_Akari_rc=Point.idol_color_dic["Kito_Akari_rc"],
            Kusunoki_Tomori_rc=Point.idol_color_dic["Kusunoki_Tomori_rc"],
            Sashide_Maria_rc=Point.idol_color_dic["Sashide_Maria_rc"],
            Tanaka_Chiemi_rc=Point.idol_color_dic["Tanaka_Chiemi_rc"],
            Koizumi_Moeka_rc=Point.idol_color_dic["Koizumi_Moeka_rc"],
            Uchida_Shu_rc=Point.idol_color_dic["Uchida_Shu_rc"],
            Houmoto_Akina_rc=Point.idol_color_dic["Houmoto_Akina_rc"],
            Yano_Hinaki_rc=Point.idol_color_dic["Yano_Hinaki_rc"],
            Date_Sayuri_rc=Point.idol_color_dic["Date_Sayuri_rc"],
            Liyuu_rc=Point.idol_color_dic["Liyuu_rc"],
            Misaki_Nako_rc=Point.idol_color_dic["Misaki_Nako_rc"],
            Payton_Naomi_rc=Point.idol_color_dic["Payton_Naomi_rc"],
            Aoyama_Nagisa_rc=Point.idol_color_dic["Aoyama_Nagisa_rc"],
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


app.run(host='0.0.0.0', debug=False, port=173)  # inami

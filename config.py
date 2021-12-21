

import json

pic_dir = 'static/picture/'

with open("data/members.json" , encoding='utf_8') as json_file:
    idol_json = json.load(json_file)
    json_file.close()

class Point():

    def __init__(self) -> None:
        self.idol_dic = {
            "Aida_Rikako": "",
            "Furihata_Ai": "",
            "Iida_Riho": "",
            "Inami_Anju": "",
            "Kobayashi_Aika": "",
            "Komiya_Arisa": "",
            "Kubo_Yurika": "",
            "Kusuda_Aina": "",
            "Mimori_Suzuko": "",
            "Nanjo_Yoshino": "",
            "Nitta_Emi": "",
            "Pile": "",
            "Saito_Shuka": "",
            "Suwa_Nanaka": "",
            "Suzuki_Aina": "",
            "Takatsuki_Kanako": "",
            "Tokui_Sora": "",
            "Uchida_Aya": "",
        }
        self.idol_color_dic = {
            "Aida_Rikako_c": "",
            "Furihata_Ai_c": "",
            "Iida_Riho_c": "",
            "Inami_Anju_c": "",
            "Kobayashi_Aika_c": "",
            "Komiya_Arisa_c": "",
            "Kubo_Yurika_c": "",
            "Kusuda_Aina_c": "",
            "Mimori_Suzuko_c": "",
            "Nanjo_Yoshino_c": "",
            "Nitta_Emi_c": "",
            "Pile_c": "",
            "Saito_Shuka_c": "",
            "Suwa_Nanaka_c": "",
            "Suzuki_Aina_c": "",
            "Takatsuki_Kanako_c": "",
            "Tokui_Sora_c": "",
            "Uchida_Aya_c": "",
        }
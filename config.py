

import json

pic_dir = 'static/picture/'

with open("data/members.json" , encoding='utf_8') as json_file:
    idol_json = json.load(json_file)
    json_file.close()

with open("data/group.json" , encoding='utf_8') as json_file:
    group_json = json.load(json_file)
    json_file.close()

class Point():

    def __init__(self) -> None:
        self.idol_group_point = {
            "μ's": 0,
            "Aqours": 0,
            "Saint Snow": 0,
            "虹ヶ咲学園スクールアイドル同好会": 0,
            "Liella": 0
        }
        self.idol_group = {
            "μ's": "",
            "Aqours": "",
            "Saint Snow": "",
            "虹ヶ咲学園スクールアイドル同好会": "",
            "Liella": ""
        }
        self.idol_color_group = {
            "μ's_c": "",
            "Aqours_c": "",
            "Saint Snow_c": "",
            "虹ヶ咲学園スクールアイドル同好会_c": "",
            "Liella_c": ""
        }
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
            "Sato_Hinata": "",
            "Tano_Asami": "",
            "Onishi_Aguri": "",
            "Sagara_Mayu": "",
            "Maeda_Kaori": "",
            "Kubota_Miyu": "",
            "Murakami_Natsumi": "",
            "Kito_Akari": "",
            "Kusunoki_Tomori": "",
            "Sashide_Maria": "",
            "Tanaka_Chiemi": "",
            "Koizumi_Moeka": "",
            "Uchida_Shu": "",
            "Houmoto_Akina": "",
            "Yano_Hinaki": "",
            "Date_Sayuri": "",
            "Liyuu": "",
            "Misaki_Nako": "",
            "Payton_Naomi": "",
            "Aoyama_Nagisa": "",
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
            "Sato_Hinata_c": "",
            "Tano_Asami_c": "",
            "Onishi_Aguri_c": "",
            "Sagara_Mayu_c": "",
            "Maeda_Kaori_c": "",
            "Kubota_Miyu_c": "",
            "Murakami_Natsumi_c": "",
            "Kito_Akari_c": "",
            "Kusunoki_Tomori_c": "",
            "Sashide_Maria_c": "",
            "Tanaka_Chiemi_c": "",
            "Koizumi_Moeka_c": "",
            "Uchida_Shu_c": "",
            "Houmoto_Akina_c": "",
            "Yano_Hinaki_c": "",
            "Date_Sayuri_c": "",
            "Liyuu_c": "",
            "Misaki_Nako_c": "",
            "Payton_Naomi_c": "",
            "Aoyama_Nagisa_c": "",
        }
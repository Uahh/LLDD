import os
import re
import requests
from get_face import cut_face

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   
        os.makedirs(path)            



idol_list = [
    "nittaemi85", "aya_uchida", "mimori_suzuko", "pile_eric", "INFO_shikaco", "rippialoha", "tokui_sorangley", "nanjolno", "kusudaaina",
    "anju_inami", "Rikako_Aida", "Saito_Shuka", "Aikyan_", "Kanako_tktk", "furihata_ai", "aina_suzuki723", "suwananaka", "box_komiyaarisa",
    "box_komiyaarisa", "satohina1223", 
    "aguri_onishi", "natyaaaaaaan07", "tomori_kusunoki", "MayuSgr", "kaor1n_n", "t_chiemi1006", "iRis_k_miyu", "kitoakari_1016", "sashide_m", "yano_hinaki35", "k_moeka_"
    "SayuriDate", "Liyu0109", "MisakiNako_", "_Naomi_Payton_", "AoyamaNagisa"
]

idol_list = [
    "nanjolno"
]

for idol in idol_list:
    jpgurl_list = []
    for page in range(1, 170):
        r = requests.get("https://twi.lovelive.cx/?id=" + idol +"&type=original&page=" + str(page))
        pattern = re.compile('https://proxy.lovelive.cx/media.+?.jpg')
        jpgurl = pattern.findall(repr(r.text))
        for i in jpgurl:
            jpgurl_list.append(i)

    jpgurl_list = list(set(jpgurl_list))

    cnt = 0
    for jpgurl in jpgurl_list:
        res = requests.get(jpgurl)
        path_list = [os.getcwd(), '\\picture\\' + idol]
        path = os.path.join(''.join(path_list))
        mkdir(path)
        path_list.append("\\")
        path_list.append(str(cnt) + '.jpg')
        file_path = os.path.join(''.join(path_list))
        with open(file_path, 'wb') as jpg_file:
            jpg_file.write(res.content)
        cnt += 1

    mkdir(path + "_cut")
    cut_face(path, path + "_cut", '.jpg', '.JPG', 'png', 'PNG')

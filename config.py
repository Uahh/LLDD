

import json

pic_dir = 'static/picture/'

with open("data/members.json", encoding='utf_8') as json_file:
    idol_json = json.load(json_file)
    json_file.close()

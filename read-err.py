



import json
import requests
import os
import time
def modify_adcode_to_id(json_data):
  print(json_data)
  for feature in json_data['features']:
    if 'properties' in feature and 'adcode' in feature['properties']:
      feature['properties']['id'] = feature['properties'].pop('adcode')
  return json_data

def to_write_file(fname,data):
  with open(fname, 'w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open('error/err.json','r',encoding='utf-8') as f:
  data = json.load(f)
  for item in data["msg"]:
    arr = item.split('-')
    code = arr[2]
    level = arr[1].split(':')[1]

    child_url = f"https://geo.datav.aliyun.com/areas_v3/bound/{code}.json"
    print('child_url:',child_url)
    child_response = requests.get(child_url)
    child_data = json.loads(child_response.text)
    child_data = modify_adcode_to_id(child_data)

    child_filename = f"{level}/{code}.json"
    to_write_file(child_filename,child_data)

    print(f"saved data for code {code} to {child_filename}")

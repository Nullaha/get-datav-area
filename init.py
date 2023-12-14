import json
import requests
import os
import time

def set_url(code):
    url =  f"https://geo.datav.aliyun.com/areas_v3/bound/{code}_full.json"
    return url

def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

def modify_adcode_to_id(json_data):
    print(json_data)
    for feature in json_data['features']:
        if 'properties' in feature and 'adcode' in feature['properties']:
            feature['properties']['id'] = feature['properties'].pop('adcode')
    return json_data

def write_to_errfile(data):
    with open("error/err.json",'a', encoding="utf-8") as err_file:
          err_file.write(data+'\n')

def to_write_file(fname,data):
    with open(fname, 'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def read_data_from_dir(dir,wantLevel):

    for filename in os.listdir(dir):
        print(filename)
        # if filename !='130000.json':
        #    continue 

        if not filename.endswith('.json'):
            continue
        filepath = os.path.join(dir,filename)

        with open(filepath,'r',encoding='utf-8') as f:
          data = json.load(f)
        child_adcodes = []
        for feature in data["features"]:
          time.sleep(1)
          try:
            adcode = feature["properties"]["id"]
            name = feature["properties"]["name"]
            level = feature["properties"]["level"]
          except KeyError as e:
              print(f"KeyError for ${feature['properties']} encountered in {filename}. Skipping this feature.")
              write_to_errfile(f"KeyError:{feature}-{filename}")
              continue
          # if wantLevel != level:
          #     print(f"我需要的level:{wantLevel}，数据中的level:{level}")
          #     write_to_errfile(f"errorLevel:wantLevel:{wantLevel}-level:{level}")
          #     continue
          if ( str(adcode) == '710000' 
              or str(adcode) == '810000' 
              or str(adcode) =='820000'
              or name == '' or not name ):
              write_to_errfile(f"{level}-{adcode}-{name}")
              continue
          create_dir(level)
          if os.path.exists(f"{level}/{adcode}.json"):
              print(f"{adcode} file already exists. Skipping.")
              continue
          
          child_url = f"https://geo.datav.aliyun.com/areas_v3/bound/{adcode}{'_full' if level !='district' else ''}.json"
          print('child_url:',child_url)
          try:
              child_response = requests.get(child_url)
              child_data = json.loads(child_response.text)
              child_data = modify_adcode_to_id(child_data)
          except (requests.RequestException,json.JSONDecodeError,UnboundLocalError) as e:
              print(f"Error fetching or decoding data for adcode {adcode}: {e}")
              write_to_errfile(f"Error-fetching:{level}-{adcode}-{name}-{e}")


          child_filename = f"{level}/{adcode}.json"
          to_write_file(child_filename,child_data)

          print(f"saved data for code {adcode} to {child_filename}")
    return
    

def get_china_data_to_dir():
  if os.path.exists('china'):
      return

  url = set_url(100000)
  print(url)
  response = requests.get(url)
  data = json.loads(response.text)
  data = modify_adcode_to_id(data)
  china_filename = f"china/100000.json"
  create_dir("china")
  to_write_file(china_filename,data)
  
  return






create_dir("error")
get_china_data_to_dir()
# read_data_from_dir('china','province')
# read_data_from_dir('province',1)


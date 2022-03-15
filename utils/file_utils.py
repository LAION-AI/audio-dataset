import json


def json_dump(data_json, json_save_path):
  with open(json_save_path, 'w') as f:
    json.dump(data_json, f)
    f.close()


def json_load(json_path):
  with open(json_path, 'r') as f:
    data = json.load(f)
    f.close()
  return data

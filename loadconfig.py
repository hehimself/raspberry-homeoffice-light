import json

with open('config.json') as config_file:
    data = json.load(config_file)

widght = data['width']
height = data['height']
print(widght)
print(height)
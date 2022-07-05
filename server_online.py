import os
import time
import yaml
import json
import requests
from config import Config

while True == True:

    config1 = Config(os.path.join('.', 'config.yaml'))
    settings = config1.get_config('settings_server')
    server_ip = settings['server_ip']
    server_port = settings['server_port']


    api_status = requests.get(f"https://api.minetools.eu/ping/{server_ip}/{server_port}")
    api_status_2 = requests.get(f"https://api.minetools.eu/query/{server_ip}/{server_port}")

    with open('minecraft_api.json', 'w') as outfile:
        json.dump(api_status.json(), outfile)
    with open('minecraft_api.json') as json_file:
        data = json.load(json_file)

    with open('minecraft_api_2.json', 'w') as outfile2:
        json.dump(api_status_2.json(), outfile2)
    with open('minecraft_api_2.json') as json_file2:
        data_2 = json.load(json_file2)

    try:
        if data['error'] == "[Errno 111] Connection refused" or data['error'] == "timed out":
            with open(os.path.join('.', 'server_status.yaml'), 'w+') as file:
                documents = yaml.dump({"server_status": {
                    "online": False,
                "players_online_now": "",
                "players_online_max": "",
                "players_online_list": ""}}, file)

            time.sleep(10)
    except:
        config = Config(os.path.join('.', 'minecraft_api.json'))
        players_online = config.get_config('players')

        with open(os.path.join('.', 'server_status.yaml'), 'w+') as file:
            try:
                documents = yaml.dump({"server_status": {
                    "online": True,
                    "players_online_now": players_online['online'],
                    "players_online_max": players_online['max'],
                    "players_online_list": data_2['Playerlist']}}, file)
            except:
                documents = yaml.dump({"server_status": {
                    "online": True,
                    "players_online_now": players_online['online'],
                    "players_online_max": players_online['max'],
                    "players_online_list": ""}}, file)

        time.sleep(10)

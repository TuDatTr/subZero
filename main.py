import sys
from os import stat
import time
from datetime import datetime

import requests
import json


def get_info():
    with open('API', 'r') as f:
        city_id = f.readline().strip('\n')
        api_key = f.readline().strip('\n')
    return [city_id, api_key]


def cache_weather():
    city_id, api_key = get_info()
    url = 'http://api.openweathermap.org/data/2.5/forecast?id={}&APPID={}&units=metric'.format(city_id, api_key)
    ob_weather = requests.get(url).text
    with open('weather_cache.json','w') as f:
        json.dump(ob_weather, f)

       
def conv_to_epoch(iso_time):
    dt_obj = datetime.strptime(iso_time, "%Y-%m-%d %H:%M:%S")
    return int(dt_obj.strftime("%s"))


def main():
    # Only request new data, when data is older than 12h
    if (time.time()-1800000>os.stat('weather_cache.json').st_mtime):
        cache_weather()
    weather = json.loads(json.load(open('weather_cache.json')))
    if(weather['cod']=='200'):
        lowest_temp = sys.maxsize
        lowest_time = ''
        for i in weather['list'][:9]:
            if lowest_temp>i['main']['temp_min']:
                lowest_temp = i['main']['temp_min']
                lowest_time = i['dt_txt']

        print(lowest_temp)
        print(lowest_time)
    else:
        print("Error.")        

if __name__ == '__main__':
    main()

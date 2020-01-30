import time 
from threading import Thread
import requests
from pymongo import MongoClient
from pprint import pprint
from weather_api.api_id import api_id

class sensor_worker(Thread):
    def run(self):
        while(True):
            lora_url = 'https://api.thingspeak.com/channels/970723/feeds.json?api_key=AU0TNWBNLRYXU1QL&results=5'
            lora_request = requests.get(lora_url).json()
            datas = lora_request["feeds"]
            data = datas[len(datas) - 1]
            
            field1 =  data["field1"]
            field2 =  data["field2"]
            field3 =  data["field3"]
            
            soil_moisture = float(field3)

            print("soil_moisture : ", soil_moisture)

            cookies = {'sysauth': '03dd9e823f79d05ff6129019918af23e'}

            mad = 30
            if(soil_moisture < mad):
                depth = 1.0
                awc = 0.21
                net_irr = awc * mad
                efficiency_of_drip = 80.0
                
                ga = net_irr / efficiency_of_drip

                area = 0.11
                flow_rate = 0.8

                # time을 분으로 환산
                irr_time = ((ga * area) / (1.6 * flow_rate)) * 3600

                str_time = str(irr_time)

                print("set time : ", irr_time)

                # trigger_request = requests.get(' http://192.168.2.241/arduino/irrigation/' + str_time, cookies=cookies)
                # print(trigger_request, "request ON")
            
            else:
                trigger_request = requests.get('http://192.168.2.241/arduino/irrigation/0', cookies=cookies)
                print(trigger_request, "request Off")
            time.sleep(5)

class weather_worker(Thread):
    def run(self):
        while(True):
            weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={},us&appid={}'
            city = 'Lafayette '
            weatehr_request = requests.get(weather_url.format(city, api_id)).json()
            print(weatehr_request)
            time.sleep(5)


def one_time_startup():
    # sensor_worker().start()
    weather_worker().start()

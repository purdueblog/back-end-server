import time 
from threading import Thread
import requests
from pymongo import MongoClient
from pprint import pprint
from weather_api.api_id import api_id
import datetime

class sensor_worker(Thread):

    def check_hour(self):
        time_api_url = 'http://worldtimeapi.org/api/timezone/America/Indiana/Indianapolis'
        time_request = requests.get(time_api_url).json()
        full_time = time_request['datetime']
        current_time = full_time[11:19]

        times = current_time.split(':')
        current_hour = 0
        current_min = 1

        print("hour : " + times[current_hour])
        print("min : " + times[current_min])

        if(int(times[current_hour]) == 9 and int(times[current_min]) < 30):
            return True
        else:
            return False
    
    def irrigation(self):
        cookies = {'sysauth': '61fe7f9775453cc3b895be0da1202af8'}
        lora_url = 'https://api.thingspeak.com/channels/970723/feeds.json?api_key=AU0TNWBNLRYXU1QL&results=5'
        lora_request = requests.get(lora_url).json()
        datas = lora_request["feeds"]
        data = datas[len(datas) - 1]
            
        field1 =  data["field1"]
        field2 =  data["field2"]
        field3 =  data["field3"]
       
        soil_moisture = float(field3)
        if(self.check_hour()):
            print("soil_moisture : ", soil_moisture)
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
                irr_time = int(((ga * area) / (1.6 * flow_rate)) * 3600)

                str_irr_time = str(irr_time)
                
                print("set time : ", irr_time)

                trigger_request = requests.get('http://192.168.2.241/arduino/irrigation/' + str_irr_time, cookies=cookies)
                print('http://192.168.2.241/arduino/irrigation/' + str_irr_time)
                print(trigger_request, "request ON")
        else:
            trigger_request = requests.get('http://192.168.2.241/arduino/irrigation/0', cookies=cookies)
            print("soil_moisture : ", soil_moisture)
            print(trigger_request, "request OFF")
    def run(self):
        while(True):
            self.irrigation()
            time.sleep(20)

class weather_worker(Thread):
    def run(self):
        # client = MongoClient('mongodb://localhost:27017')
        # print(client)
        # db = client.irrigation
        # print(db)
        # serverStatusResult=db.command("serverStatus")
        # print("hello\n\n\n")
        # pprint(serverStatusResult)

        weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={},us&appid={}'
        city = 'Lafayette '
        weatehr_request = requests.get(weather_url.format(city, api_id)).json()
        print(weatehr_request)

        # while(True):
        #     weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={},us&appid={}'
        #     city = 'Lafayette '
        #     weatehr_request = requests.get(weather_url.format(city, api_id)).json()
        #     print(weatehr_request)
        #     time.sleep(5)


def one_time_startup():
    sensor_worker().start()
    # weather_worker().start()

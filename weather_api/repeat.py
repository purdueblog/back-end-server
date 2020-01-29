import time
from threading import Thread
import requests

class worker(Thread):
    def run(self):
        while(True):
            lora_url = 'https://api.thingspeak.com/channels/956974/feeds.json?api_key=ZRTL71SHNNFL0KJ0&results=8000'
            lora_request = requests.get(lora_url).json()
            datas = lora_request["feeds"]
            data = datas[len(datas) - 1]
            
            field1 =  data["field1"]
            field2 =  data["field2"]
            field3 =  data["field3"]
            
            soil_moisture = int(field3) / 8

            print(soil_moisture)

            cookies = {'sysauth': 'c03412f3ac67293cb346e0896b52acc9'}

            mad = 50
            if(soil_moisture < mad):
                depth = 1
                awc = 0.11
                net_irr = awc * mad
                efficiency_of_drip = 80
                ga = net_irr / efficiency_of_drip

                area = 16
                flow_rate = 1.6
                time = (ga * area) / (1.6 * flow_rate)

                trigger_request = requests.get('http://192.168.43.69/arduino/1', cookies=cookies)
                print(trigger_request, "request ON")
            
            else:
                trigger_request = requests.get('http://192.168.43.69/arduino/0', cookies=cookies)    
                print(trigger_request, "request Off")
            
            time.sleep(10)


def one_time_startup():
    worker().start()
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
            
            soilMoisture = int(field3) / 8

            print(soilMoisture)

            if(soilMoisture < 60):
                cookies = {'sysauth': 'c03412f3ac67293cb346e0896b52acc9'}
                trigger_request = requests.get('http://192.168.43.69/arduino/1', cookies=cookies)
                print(trigger_request, "request ON")
            
            else:
                cookies = {'sysauth': 'c03412f3ac67293cb346e0896b52acc9'}
                trigger_request = requests.get('http://192.168.43.69/arduino/0', cookies=cookies)    
                print(trigger_request, "request Off")
            
            time.sleep(10)


def one_time_startup():
    worker().start()
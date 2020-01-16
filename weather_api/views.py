from rest_framework.views import APIView
from rest_framework.response import Response
from weather_api.api_id import api_id
import requests

class WeatherApi(APIView):
    def get(self, request, format=None):
        weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={},us&appid={}'
        lora_url = 'https://api.thingspeak.com/channels/956974/feeds.json?api_key=ZRTL71SHNNFL0KJ0&results=8000'
        city = 'Lafayette'
        weatehr_request = requests.get(weather_url.format(city, api_id)).json()
        # lora_request = requests.get(lora_url).json()
        lora_request = "None"
        
        # 웹에서 로그인 후 발급받는 쿠키값 이용하여 api 이용
        cookies = {'sysauth': 'e2187037cd9cc3722af5e4159d905121'}
        trigger_request = requests.get('http://192.168.43.69/arduino/irrigation/control/off', cookies=cookies)
        
        return Response({'message' : weatehr_request, 'lora' : lora_request, "trigger" : trigger_request})

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
        lora_request = requests.get(lora_url).json()
        return Response({'message' : weatehr_request, 'lora' : lora_request})

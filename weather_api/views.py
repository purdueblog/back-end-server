from rest_framework.views import APIView
from rest_framework.response import Response
from weather_api.api_id import api_id
from background_task import background
import requests
from pymongo import MongoClient

class WeatherApi(APIView):
    
    def get(self, request, format=None):
        return Response({'message' : "weatehr_request"})

class IrrigationApi(APIView):
    
    def get(self, request, format=None):
        # cluster = MongoClient("mongodb+srv://myungwoo:didhk7339@cluster0-hrdwg.mongodb.net/test?retryWrites=true&w=majority")
        # db = cluster["irrigation"]
        # collection = db["irrigation"]
        print(request)
        return Response({'message' : "hello"})


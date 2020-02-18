from rest_framework.views import APIView
from rest_framework.response import Response
from weather_api.api_id import api_id
from background_task import background
import requests
from pymongo import MongoClient
import datetime

class WeatherApi(APIView):
    
    def get(self, request, format=None):
        return Response({'message' : "weatehr_request"})

class IrrigationApi(APIView):
    
    def get(self, request, format=None):
        
        start_day_key = '0'
        end_day_key = '4'
        year_key = 'year'

        month_index = 0
        day_index = 1

        data = request.query_params

        year = data[year_key]

        start_date = data[start_day_key].split("/") 
        end_date = data[end_day_key].split("/") 

        if(start_date[month_index] != '0'):
            cluster = MongoClient("mongodb+srv://myungwoo:didhk7339@cluster0-hrdwg.mongodb.net/test?retryWrites=true&w=majority")
            db = cluster["irrigation"]
            collection = db["irrigation"]

            result = collection.find()

            # set date range
            start = datetime.datetime(int(year), int(start_date[month_index]), int(start_date[day_index]), 0, 0)
            end = datetime.datetime(int(year), int(end_date[month_index]), int(end_date[day_index]), 23, 59)
            print(start)
            print(end)
            # fetch irrigation data by range
            # result = collection.find({'dt': {'$lt': end, '$gte': start}})
            # print("request data : ", request.query_params[start_day_key], request.query_params[end_day_key])
            print(result)
            # for row in result:
            #     print(row[0])

            index = 0
            while(True):
                try:
                    result[index]
                except IndexError:
                    break
                print("loop")
                print(result[index])
                index += 1
        return Response({'message' : "hello"})


        


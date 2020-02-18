from rest_framework.views import APIView
from rest_framework.response import Response
from weather_api.api_id import api_id
from background_task import background
import requests
from pymongo import MongoClient
import datetime
import math

class WeatherApi(APIView):
    
    def get(self, request, format=None):
        return Response({'message' : "weatehr_request"})

class IrrigationApi(APIView):


    def get_index(self, days, today):
        for i in range(len(days)):
            if(days[i] == today):
                return i
        return 0 
    
    def fetch_data(self, year, start_date, end_date):
        month_index = 0
        day_index = 1

        cluster = MongoClient("mongodb+srv://myungwoo:didhk7339@cluster0-hrdwg.mongodb.net/test?retryWrites=true&w=majority")
        db = cluster["irrigation"]
        collection = db["irrigation"]
        
        # set date range
        start = datetime.datetime(int(year), int(start_date[month_index]), int(start_date[day_index]), 0, 0)
        end = datetime.datetime(int(year), int(end_date[month_index]), int(end_date[day_index]), 23, 59)
        
        # fetch irrigation data by range
        result = collection.find({'dt': {'$lt': end, '$gte': start}})
        return result

    
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
            
            print("request data : ", request.query_params[start_day_key], request.query_params[end_day_key])

            result = self.fetch_data(year, start_date, end_date)

            print(result)
        
            day_list = [0] * 5
            day_length = 5

            # make list about day
            for i in range(day_length):
                day_list[i] = int(data[str(i)].split("/")[day_index])

            water_of_days = [0] * 5
            index = 0
            
            # make list about total amout of irrigation water
            while(True):
                try:
                    result[index]
                except IndexError:
                    break
                day = result[index]['dt'].day
                water = result[index]['water']
                input_index = self.get_index(day_list, day)
                water_of_days[input_index] += water
                index += 1
    

        return Response({'message' : "hello"})


        


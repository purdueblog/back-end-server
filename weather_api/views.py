from rest_framework.views import APIView
from rest_framework.response import Response
from weather_api.api_id import api_id
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

    def last_day_of_month(self, any_day):
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)


    def fetch_all_data(self, year, start_date, end_date):
        month_index = 0
        day_index = 1

        cluster = MongoClient("mongodb+srv://myungwoo:didhk7339@cluster0-hrdwg.mongodb.net/test?retryWrites=true&w=majority")
        db = cluster["irrigation"]
        collection = db["irrigation"]
        
        # set date range
        start = datetime.datetime(int(year), int(start_date[month_index]), 1, 0, 0)
        end = self.last_day_of_month(start)
        
        # fetch irrigation data by range
        result = collection.find()
        return result

    # return : list 
    def fetch_range_data(self, year, start_date, end_date, datas):
        month_index = 0
        day_index = 1

        cluster = MongoClient("mongodb+srv://myungwoo:didhk7339@cluster0-hrdwg.mongodb.net/test?retryWrites=true&w=majority")
        db = cluster["irrigation"]
        collection = db["irrigation"]

        # set date range
        start = datetime.datetime(int(year), int(start_date[month_index]), 1, 0, 0)
        end = datetime.datetime(int(year), int(end_date[month_index]), int(end_date[day_index]), 23, 59)        

        # init container
        result = []
        index = 0
        while(True):
            try:
                datas[index]
            except IndexError:
                break
            if(start <= datas[index]['dt'] and datas[index]['dt'] <= end):
                result.append(datas[index])

            index += 1

        # fetch irrigation data by range
        print(end)
        return result
    
    # return : float
    def get_month_water(self, datas):
        sum = 0
        for data in datas:
            sum += data['water']
        return sum
    
    def get(self, request, format=None):
        
        # key for url params
        start_day_key = '0'
        end_day_key = '4'
        year_key = 'year'

        month_index = 0
        day_index = 1

        data = request.query_params

        year = data[year_key]

        start_date = data[start_day_key].split("/") 
        end_date = data[end_day_key].split("/") 

        # check init data
        if(start_date[month_index] != '0'):
            
            # get all data
            datas = self.fetch_all_data(year, start_date, end_date)
            
            # get data by range
            datas_by_range = self.fetch_range_data(year, start_date, end_date, datas)


            day_length = 5
            day_list = [0] * day_length

            # make list about day
            for i in range(day_length):
                day_list[i] = int(data[str(i)].split("/")[day_index])

            water_of_days = [0] * day_length
            index = 0

            # make list about total amout of irrigation water
            while(True):
                try:
                    datas_by_range[index]
                except IndexError:
                    break
                day = datas_by_range[index]['dt'].day
                water = datas_by_range[index]['water']
                input_index = self.get_index(day_list, day)
                water_of_days[input_index] += water
                index += 1

            month_water = self.get_month_water(datas)
            print(month_water)
            return Response({'waters' : water_of_days, 'monthWater' : month_water})

        init_value = [0,0,0,0,0,0]
        return Response({'waters' : init_value, 'monthWater' : 0})



        


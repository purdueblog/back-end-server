from django.urls import path
from weather_api import views

urlpatterns = [
    path('weather', views.WeatherApi.as_view()),
]
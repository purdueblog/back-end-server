from django.urls import path
from weather_api import views
from weather_api import repeat

urlpatterns = [
    path('weather', views.WeatherApi.as_view()),
    path('irrigation', views.IrrigationApi.as_view()),
]

# repeat.one_time_startup()
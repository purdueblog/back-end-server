import requests
import isodate

def get_iso_current_time():
    time_api_url = 'http://worldtimeapi.org/api/timezone/America/Indiana/Indianapolis'
    time_request = requests.get(time_api_url).json()
    full_time = time_request['datetime']
    current_isodate = isodate.parse_datetime(full_time[:-6])
    return current_isodate
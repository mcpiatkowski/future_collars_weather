import requests
import json
import sys
import datetime


def find_date():
    if len(sys.argv) > 2:
        date_to_check = sys.argv[2][:10]
    else:
        today = datetime.date.today()
        date_to_check = today + datetime.timedelta(days=1)
    return str(date_to_check)
    

def check_weather_in_dict(date_to_check, weather_dict):
    fall = False
    date_exists = False
    for item in range(weather_dict["elblag,pl"]["cnt"]):
        description = weather_dict["elblag,pl"]["list"][item]['weather'][0]['description']
        description_time = weather_dict["elblag,pl"]["list"][item]['dt_txt'][:10]
        if description_time == date_to_check:
            date_exists = True
            if 'snow' in description:
                fall = True
                return fall, date_exists
    return fall, date_exists


def download_new_weather_data(key):
    url = "https://community-open-weather-map.p.rapidapi.com/forecast"

    querystring = {"q":"elblag,pl"}

    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


def print_forecast(fall, date_exists):
    if fall:
        print('Będzie padać.')
    elif not fall and date_exists:
        print('Nie będzie padać.')
    else:
        print('Nie wiem.')

    
def main():
    key = sys.argv[1]
    with open('output.json') as input:
        weather_dict = json.load(input)
    date_to_check = find_date()
    fall, date_exists = check_weather_in_dict(date_to_check, weather_dict)
    if not date_exists:
        weather_dict["elblag,pl"] = download_new_weather_data(key)
        fall, date_exists = check_weather_in_dict(date_to_check, weather_dict)
        with open('output.json', 'w') as output:
            output.write(json.dumps(weather_dict))
    print_forecast(fall, date_exists)
    

if __name__ == '__main__':
    main()
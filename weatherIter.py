import json
import requests
from sys import argv
from credentials import key
from datetime import date, timedelta


class WeatherForecast:
    def __init__(self, key):
        self.key = key
        self.cache = {}
        self.city = "elblag"


    def __iter__(self):
        return iter(self.cache[self.city].keys())


    def __getitem__(self, date):
        return self.cache[self.city][date]


    def __setitem__(self, date, new_value):
        self.cache[self.city][date] = new_value


    def items(self):
        for date, forecast in self.cache[self.city].items():
            yield ('{}, {}'.format(date, forecast))

    
    def read_cache(self):
        with open('cache.json') as cache:
            self.cache = json.load(cache)


    def download_data(self):
        url = "https://community-open-weather-map.p.rapidapi.com/forecast"

        querystring = {"q": self.city}

        headers = {
            'x-rapidapi-key': self.key,
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()


    def update_cache(self, new_data):
        for item in range(new_data["cnt"]):
            date = new_data['list'][item]['dt_txt'][:10]
            if ('snow' or 'rain') in new_data['list'][item]:
                self.cache[self.city][date] = 'bedzie padac'
            else:
                 self.cache[self.city][date] = 'nie bedzie padac'
        with open('cache.json', 'w') as cache:
            cache.write(json.dumps(self.cache))
    

    def get_forecast_date(self, argv):
        if len(argv) > 1:
            date_to_check = argv[1][:10]
        else:
            today = date.today()
            date_to_check = today + timedelta(days=1)
        return str(date_to_check)


def main():
    wf = WeatherForecast(key)
    date = wf.get_forecast_date(argv)
    wf.read_cache()
    if not date in wf:
        new_data = wf.download_data()
        wf.update_cache(new_data)
    if date in wf:
        print(wf[date])
    else:
        print('Nie wiem.')


if __name__ == '__main__':
    main()
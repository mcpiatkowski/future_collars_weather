import credentials
import json

class WeatherForecast:
    def __init__(self, key):
        self.key = key
        self.cache = {}
        self.city = 'stegna'


    def __iter__(self):
        return iter(self.cache[self.city].keys())


    def __getitem__(self, date):
        return self.cache[self.city][date]


    def __setitem__(self, date, new_value):
        self.cache[self.city][date] = new_value


    def items(self):
        for date, forecast in self.cache[self.city].items():
            yield ('{}, {}'.format(date, forecast))

    
    def read_data(self):
        with open('test.json') as checked_weather:
            self.cache = json.load(checked_weather)


wf = WeatherForecast(credentials.key)

wf.read_data()

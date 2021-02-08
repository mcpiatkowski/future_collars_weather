import requests
import json
import sys
import datetime

count = 0
date_exists = False

if len(sys.argv) > 1:
    date = sys.argv[1][:10]
else:
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)



with open('output.json') as input:
    weather_dict = json.load(input)

weather_in_elblag = weather_dict["elblag,pl"]["list"]

for city in weather_dict.keys():
    print(city)


print("length_list: ", len(weather_dict["elblag,pl"]["list"]))

print(weather_dict["elblag,pl"]["list"][2]['weather'][0]['description'])

for item in range(weather_dict["elblag,pl"]["cnt"]):
    description = weather_dict["elblag,pl"]["list"][item]['weather'][0]['description']
    description_time = weather_dict["elblag,pl"]["list"][item]['dt_txt'][:10]
    if description_time == date:
        date_exists = True
        print('Description: {}, Date: {}'.format(description, description_time))
        if 'snow' in description:
            count +=1

print('count: ', count)

if count > 0:
    print('Będzie padać.')
elif count == 0 and date_exists == True:
    print('Nie będzie padać.')
else:
    print('Nie wiem.')
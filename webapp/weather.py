import requests
from flask import current_app


def weather_by_city(city_name):
    weather_url = current_app.config['WEATHER_URL']
    params = {
        "key": current_app.config['WEATHER_API_KEY'],
        "q": city_name,
        "format": "json",
        "num_of_days": 1,
        "lang": "ru"
    }
    try:
        result = requests.get(weather_url, params=params)
        result.raise_for_status()
        weather_data = result.json()
        if 'data' in weather_data:
            if 'current_condition' in weather_data['data']:
                try:
                    return weather_data['data']['current_condition'][0]
                except(IndexError, TypeError):
                    return False
        return False
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


if __name__ == "__main__":
    print(weather_by_city("Moscow,Russia"))

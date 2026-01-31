import requests

headers = {
    "User-Agent": "current-weather/1.0 (indigoprzybylski@gmail.com)",
    "Accept": "application/geo+json"
}

class HourlyForecast:

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def get_hourly_forecast_json(self) -> dict[str, any]:
        # api url for the given coordinates
        api_url = f"https://api.weather.gov/points/{self.lat},{self.lon}"
        # fetch the api response, raise for status
        api_response = requests.get(api_url, headers=headers)
        api_response.raise_for_status()
        # unpack api response into a json object
        api_response_data = api_response.json()
        # extracting the hourly forecast url from the api response
        hourly_forecast_url = api_response_data['properties']['forecastHourly']
        # fetch the hourly forecast from the api, raise for status
        hourly_forecast_response = requests.get(hourly_forecast_url, headers=headers)
        hourly_forecast_response.raise_for_status()
        # unpack the api response into a json object
        hourly_forecast_data = hourly_forecast_response.json()
        return hourly_forecast_data

    def get_hourly_forecast_data(self, num_hours: int = 12, step: int = 2) -> list[list[any]]:
        # get the forecast JSON
        forecast_json = self.get_hourly_forecast_json()
        data: list[list[any]] = [] # format: [timestamp, temp, description]
        for period in forecast_json['properties']['periods'][:num_hours:step]:
            period_data: list[any] = []
            period_data.append(period['startTime'][11:16]) # timestamp
            period_data.append(f"{period['temperature']:>3}°{period['temperatureUnit']}") # temperature
            period_data.append(period['shortForecast'])
            data.append(period_data)
        return data
        
    def print_forecast(self, num_hours: int = 12, step: int = 2) -> None:
        data = self.get_hourly_forecast_data(num_hours=num_hours, step=step)
        for time in data:
            print(f"{time[0]}:{time[1]} | {time[2]}")
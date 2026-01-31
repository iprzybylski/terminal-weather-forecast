import requests

headers = {
    "User-Agent": "weather-forecast-test/1.0 (indigoprzybylski@gmail.com)",
    "Accept": "application/geo+json"
}



lat = 42.390
lon = -72.527  # Amherst, MA

class MultidayForecast:

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def get_multiday_forecast_json(self) -> dict[str, any]:

        url = f"https://api.weather.gov/points/{lat},{lon}"

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        forecast_url = data["properties"]["forecast"]

        forecast_response = requests.get(forecast_url, headers=headers)
        forecast_response.raise_for_status()

        forecast_data = forecast_response.json()
        return forecast_data
    
    def get_multiday_forecast_data(self, num_days: int = 5) -> list[list[any]]:
        # get the forecast data
        forecast_data = self.get_multiday_forecast_json()
        is_day = forecast_data['properties']['periods'][0]['name'] != 'Tonight'
        data: list[list[any]] = []
        for period in forecast_data["properties"]["periods"][(1 if is_day else 0):num_days*2:2]:
            period_data: list[any] = []
            period_data.append(period['name'])
            period_data.append(f"{period['temperature']:>2}°F")
            period_data.append(period['shortForecast'])
            data.append(period_data)
        return data

    def print_forecast(self, num_days: int = 5) -> None:

        forecast_data = self.get_multiday_forecast_json()

        is_day = forecast_data['properties']['periods'][0]['name'] != 'Tonight'

        for period in forecast_data["properties"]["periods"][(1 if is_day else 0):num_days*2:2]:
            print(f"{period["name"]:>10} | {period["temperature"]:^3}F | {period["shortForecast"]}")

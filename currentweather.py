import requests

headers = {
    "User-Agent": "current-weather/1.0 (indigoprzybylski@gmail.com)",
    "Accept": "application/geo+json"
}

"""Class for getting current weather observations from NWS stations"""
class CurrentWeather:
    
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        self.station_json = self.get_station_json()

    def get_station_json(self) -> dict[str, str | dict]:
        # api url for the given coordinates
        api_url = f"https://api.weather.gov/points/{self.lat},{self.lon}"
        # fetch the api response, raise for status
        api_response = requests.get(api_url, headers=headers)
        api_response.raise_for_status()
        # unpack api response into a json object
        api_response_data = api_response.json()
        # get the stations url from the api data
        stations_url = api_response_data['properties']['observationStations']
        # fetch api response, raise for status
        stations_response = requests.get(stations_url, headers=headers)
        stations_response.raise_for_status()
        # unpack api response into a json object
        stations_data = stations_response.json()
        # pull the nearest station from the data, and return it :)
        station = stations_data['features'][0]
        return station
    
    def get_current_weather_json(self) -> dict[str, str | dict]:
        # get the precomputed station json
        station_data = self.station_json
        # get the station id
        station_id = station_data['properties']['stationIdentifier']
        # api endpoint for latest observation
        observation_url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
        # get the api response for the latest observation, raise for status
        observation_response = requests.get(observation_url, headers=headers)
        observation_response.raise_for_status()
        # unpack api response into a json object, return
        observation_data = observation_response.json()
        return observation_data
    
    def get_current_temp(self, units='C') -> int:
        current_weather = self.get_current_weather_json()
        temp_dict = current_weather['properties']['temperature']
        temp = temp_dict['value']
        if units == 'F':
            temp = temp * 9/5 + 32
        elif units == 'K':
            temp = temp + 273
        return round(temp)
    
    def get_weather_description(self) -> str:
        current_weather = self.get_current_weather_json()
        description = current_weather['properties']['textDescription']
        return description
    
    def get_weather(self) -> str:
        return f"{self.get_current_temp(units='F')}°F | {self.get_weather_description()}"
    
    def print_weather(self) -> None:
        print(self.get_weather())
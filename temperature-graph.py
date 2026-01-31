import matplotlib.pyplot as plt
import numpy as np
import requests

class TemperatureData:

    def __init__(self, lat: float, lon: float, headers: dict[str, str] = {
                "User-Agent": "weather-forecast-test/1.0 (indigoprzybylski@gmail.com)",
                "Accept": "application/geo+json"
            }):
        self.lat = lat
        self.lon = lon
        self.headers = headers
        self.temps = self.get_temps_array()

    def get_hourly_forecast_json(self) -> dict[str, any]:
        # api url for the given coordinates
        api_url = f"https://api.weather.gov/points/{self.lat},{self.lon}"
        # fetch the api response, raise for status
        api_response = requests.get(api_url, headers=self.headers)
        api_response.raise_for_status()
        # unpack api response into a json object
        api_response_data = api_response.json()
        # get the hourly forecast url from the api data
        hourly_forecast_url = api_response_data['properties']['forecastHourly']
        # fetch the hourly forecast data from the forecast url, raise for status
        hourly_forecast_response = requests.get(hourly_forecast_url, headers=self.headers)
        hourly_forecast_response.raise_for_status()
        # convert to json object
        hourly_forecast_data = hourly_forecast_response.json()
        # return the data
        return hourly_forecast_data
    
    def get_temps_array(self) -> np.ndarray:
        # get forecast data
        data = self.get_hourly_forecast_json()
        # create list of temps
        temps: list[int] = []
        # go through each timestep in the data
        for period in data['properties']['periods']:
            temps.append(period['temperature'])
        # return the list as a numpy array for speed
        return np.array(temps)
    
    def __repr__(self) -> str:
        return f"{self.temps}"


class TemperatureGraph:

    def __init__(self, temp_data: TemperatureData):
        self.temp_data = temp_data
    
    def create_graph(self) -> None:
        # get the temperature data
        temps: np.ndarray = self.temp_data.get_temps_array()
        # draw temperature line
        plt.plot(temps, 'g-')
        plt.axis((0, temps.size, -20, 40)) # -20F to 120F
        # find maxima and minima and label them (a little bit janky!)
        # TODO use np.argmin and np.argmax to find these more effectively :P
        for i in range(1, temps.size - 1):
            if temps[i] > temps[i - 1] and temps[i] >= temps[i + 1]:
                plt.plot(i, temps[i], 'ro')
                plt.text(i + 2, temps[i] + 2, temps[i], color='red')
            if temps[i] <= temps[i - 1] and temps[i] < temps[i + 1]:
                plt.plot(i, temps[i], 'bo')
                plt.text(i + 2, temps[i] + 2, temps[i], color='blue')
        # display the graph
        plt.show()


td = TemperatureData(42.39, -72.52) # Amherst, MA
tg = TemperatureGraph(td)
tg.create_graph()
from currentweather import CurrentWeather
from hourlyforecast import HourlyForecast
from multidayforecast import MultidayForecast

lat = 42.390
lon = -72.527  # Amherst, MA

class WeatherToday:

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        self.currweather = CurrentWeather(lat, lon)
        self.hourly = HourlyForecast(lat, lon)
        self.multi = MultidayForecast(lat, lon)

    def print_todays_weather(self) -> None:
        print("----------\nCurrent Weather\n----------")
        self.currweather.print_weather()
        print("----------\nNext Few Hours\n----------")
        self.hourly.print_forecast()
        print("----------\nNext Few Days\n----------")
        multi_data = self.multi.get_multiday_forecast_data(num_days=3)
        for day in multi_data:
            print(f"{day[0][:3]}: {day[1]} | {day[2]}")
        print("----------")

w = WeatherToday(lat, lon)
w.print_todays_weather()
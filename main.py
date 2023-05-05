from data_loader import Loader
from mapping import Map
import matplotlib.pyplot as plt


if __name__ == '__main__':
    data = Loader("data/bike_journeys.csv", "data/weather.csv", "data/bike_stations.csv")

    cords = [51.5072, -0.1276]
    bike_map = Map(cords, 10)
    for index, row in data.locations.iterrows():
        bike_map.add_station(row["Coordinates"], row["Station Name"])
    # bike_map.plot_shortest_cycle_route()
    bike_map.show_map()

    plt.scatter(data.daily["TAVG (CELSIUS)"], data.daily["JOURNEYS"])
    plt.show()


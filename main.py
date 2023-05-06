from data_loader import Loader
from mapping import Map, ScaleGenerator
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = Loader("data/bike_journeys.csv", "data/weather.csv", "data/bike_stations.csv")
    max_visitors = data.locations["Visitors"].max()
    min_visitors = data.locations["Visitors"].min()
    scale_generator = ScaleGenerator(max_visitors, min_visitors)

    center_cords = [51.5020605, -0.119522]
    bike_map = Map(center_cords, 12.5, scale_generator)
    for index, row in data.locations.iterrows():
        # Problem of incomplete data -> move to mapper?
        # Add log
        if type(row["Coordinates"]) is tuple:
            bike_map.add_station(row["Coordinates"], row["Station Name"], row["Visitors"])
    bike_map.plot_shortest_cycle_route((-0.10997, 51.529163), (-0.136039, 51.519914))
    bike_map.plot_shortest_cycle_route((-0.125979, 51.526357), (-0.105344, 51.515059))
    bike_map.show_map()

    plt.scatter(data.daily["TAVG (CELSIUS)"], data.daily["JOURNEYS"])
    plt.show()


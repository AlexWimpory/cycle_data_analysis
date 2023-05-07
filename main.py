from data_loader import Loader
from mapping import Map, ScaleGenerator
import config

if __name__ == '__main__':
    # Load and process csv files
    data = Loader("data/bike_journeys.csv", "data/weather.csv", "data/bike_stations.csv")
    # Create object which scales colour and size between the max and min numbers
    max_visitors, min_visitors = data.calculate_max_min_visitors()
    scale_generator = ScaleGenerator(max_visitors, min_visitors)
    # Create a Map object which handles osmnx and folium
    bike_map = Map(config.center_cords, config.zoom_start, scale_generator)
    # Add stations to the map
    bike_map.add_stations(data.locations)
    # Find and plot shortest route between cords
    bike_map.plot_shortest_cycle_route((-0.10997, 51.529163), (-0.136039, 51.519914))
    bike_map.plot_shortest_cycle_route((-0.125979, 51.526357), (-0.105344, 51.515059))
    # Open map in browser
    bike_map.show_map()




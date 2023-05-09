from data_loader import Loader
from mapping import Map, ScaleGenerator
from graphs import plot_temp_vs_journeys
import config

###
# See speaker notes of the presentation to find a discussion of the output
###

if __name__ == '__main__':
    # Load and process csv files
    data = Loader("data/bike_journeys.csv", "data/weather.csv", "data/bike_stations.csv")
    data.generate_route()
    # Create object which scales colour and size between the max and min numbers
    max_visitors, min_visitors = data.calculate_max_min_visitors()
    scale_generator = ScaleGenerator(max_visitors, min_visitors)
    # Create a Map object which handles osmnx and folium
    bike_map = Map(config.center_cords, config.zoom_start, scale_generator)

    # Add stations to the map
    bike_map.add_stations(data.locations)
    # Find and plot shortest route between cords
    bike_map.plot_shortest_cycle_route((-0.10997, 51.529163), (-0.136039, 51.519914), "blue")
    bike_map.plot_shortest_cycle_route((-0.10997, 51.529163), (-0.136039, 51.519914), "blue")

    # # Plot most used routes excluding round trips
    # routes = data.calculate_common_routes(10, 20)
    # bike_map.plot_cycle_routes(routes)

    # Open map in browser
    bike_map.show_map()

    plot_temp_vs_journeys(data)




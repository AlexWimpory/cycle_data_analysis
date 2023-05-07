import math
import folium
import webbrowser
import osmnx as ox
from osmnx import distance
import networkx as nx
import branca.colormap as cmp
import config


# TODO No path exception

def generate_cycle_network(side_1, side_2, side_3, side_4):
    """
    Use OSMN data to generate a network of bike paths from long/lat boundaries
    :param side_1: northern latitude
    :param side_2: southern latitude
    :param side_3: eastern longitude
    :param side_4: western longitude
    """
    graph_data = ox.graph_from_bbox(side_1, side_2, side_3, side_4, network_type="bike", retain_all=True)
    # Save as such a large and detailed network takes a while to download
    ox.save_graphml(graph_data, config.network_path)


def generate_main_roads_network(side_1, side_2, side_3, side_4):
    graph_data = ox.graph_from_bbox(side_1, side_2, side_3, side_4, network_type='drive',
                                    custom_filter='["highway"~"primary"]', retain_all=True)
    ox.save_graphml(graph_data, config.network_path)


class Map:
    def __init__(self, center, zoom_start, scale_generator):
        self.center = center
        self.zoom_start = zoom_start
        # Create map
        self.map = folium.Map(location=self.center, zoom_start=self.zoom_start)
        self.scale_generator = scale_generator
        # Load network
        self.graph_data = ox.load_graphml(config.network_path)

    def show_map(self):
        print("Loading map")
        # Add scale to the map
        self.scale_generator.linear.add_to(self.map)
        folium.TileLayer(config.map_style).add_to(self.map)
        # Save map as html and open in browser
        self.map.save(config.map_name)
        webbrowser.open(config.map_name)

    def add_station(self, location, name, visitors):
        """
        Add a circle onto the map
        :param visitors: int used for colour and size scale
        :param location: tuple containing longitude and latitude
        :param name: string for popup
        """
        # Check for missing data
        if math.isnan(visitors):
            print(f"{name} has no visitors data")
        else:
            folium.Circle(
                radius=self.scale_generator.calculate_size(visitors),
                location=location,
                popup=name,
                color=self.scale_generator.calculate_colour(visitors),
                fill=True,
            ).add_to(self.map)

    def add_stations(self, locations):
        """
        Step through location data, adding a station to the map for each entry
        """
        for index, row in locations.iterrows():
            # Check for missing data
            if type(row["Coordinates"]) is tuple:
                self.add_station(row["Coordinates"], row["Station Name"], row["Visitors"])
            else:
                print(f"Station ID '{row['Station ID']}' location not known")

    def plot_network(self):
        """
        Plot lines on the map for the network. WARNING - not advisable for large networks as it will
        take a long time to load
        """
        ox.plot_graph_folium(self.graph_data, self.map, popup_attribute="name", weight=2, color="#8b0000")

    def find_node(self, cords):
        """
        Find the nearest node of specified coordinates in a network.  Uses a k-d tree for euclidean nearest
        neighbor search and requires scikit-learn be installed
        """
        print(f"Finding node {cords}")
        node = ox.distance.nearest_nodes(self.graph_data, cords[0], cords[1])
        return node

    def plot_shortest_cycle_route(self, start, end):
        """
        Find the shortest path between 2 nodes using networkx and Dijkstra’s algorithm
        """
        print("Calculating shortest route")
        route = nx.shortest_path(self.graph_data, self.find_node(start), self.find_node(end))
        ox.plot_route_folium(self.graph_data, route, self.map, weight=10)


class ScaleGenerator:
    """
    Scale colour and size, based on max and min numbers
    """
    def __init__(self, max_visitors, min_visitors):
        self.max_visitors = max_visitors
        self.min_visitors = min_visitors
        # Continuous set of colours
        self.linear = cmp.LinearColormap(
            [config.circle_colour_1, config.circle_colour_2],
            vmin=self.min_visitors, vmax=self.max_visitors,
            caption='Visitors over 50 days'
        )

    def calculate_colour(self, visitors):
        # Output colour as a red,green,blue,alpha hex value
        return self.linear.rgba_hex_str(visitors)

    def calculate_size(self, visitors):
        # Scale radius size
        scale = visitors / (self.max_visitors - self.min_visitors)
        radius = ((config.max_circle_radius - config.min_circle_radius) * scale) + config.min_circle_radius
        return radius


if __name__ == '__main__':
    generate_cycle_network(51.550267, 51.453854, -0.00083, -0.238211)
    # generate_main_roads_network(51.550267, 51.453854, -0.00083, -0.238211)

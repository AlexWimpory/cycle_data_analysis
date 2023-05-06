import math
import folium
import webbrowser
import osmnx as ox
import networkx as nx
import branca.colormap as cmp
from osmnx import distance
import config


# TODO No path exception
# TODO Logging

def generate_cycle_network(side_1, side_2, side_3, side_4):
    graph_data = ox.graph_from_bbox(side_1, side_2, side_3, side_4, network_type="bike", retain_all=True)
    ox.save_graphml(graph_data, "data/network.graphml")


def generate_main_roads_network(side_1, side_2, side_3, side_4):
    graph_data = ox.graph_from_bbox(side_1, side_2, side_3, side_4, network_type='drive',
                                    custom_filter='["highway"~"primary"]', retain_all=True)
    ox.save_graphml(graph_data, "data/network.graphml")


class Map:
    def __init__(self, center, zoom_start, scale_generator):
        self.center = center
        self.zoom_start = zoom_start
        # Create map
        self.map = folium.Map(location=self.center, zoom_start=self.zoom_start)
        self.scale_generator = scale_generator
        # Load network
        self.graph_data = ox.load_graphml("data/network.graphml")

    def show_map(self):
        print("Loading map")
        self.scale_generator.linear.add_to(self.map)
        folium.TileLayer(config.map_style).add_to(self.map)
        self.map.save("map.html")
        webbrowser.open("map.html")

    def add_station(self, location, name, visitors):
        """
        Add a marker onto the map
        :param visitors:
        :param location: tuple containing longitude and latitude
        :param name: string for popup
        """
        if math.isnan(visitors):
            pass
        else:
            folium.Circle(
                radius=self.scale_generator.calculate_size(visitors),
                location=location,
                popup=name,
                color=self.scale_generator.calculate_colour(visitors),
                fill=True,
            ).add_to(self.map)

    def plot_network(self):
        ox.plot_graph_folium(self.graph_data, self.map, popup_attribute="name", weight=2, color="#8b0000")

    def find_node(self, cords):
        print(f"Finding node {cords}")
        node = ox.distance.nearest_nodes(self.graph_data, cords[0], cords[1])
        return node

    def plot_shortest_cycle_route(self, start, end):
        print("Calculating shortest route")
        route = nx.shortest_path(self.graph_data, self.find_node(start), self.find_node(end))
        ox.plot_route_folium(self.graph_data, route, self.map, weight=10)


class ScaleGenerator:
    def __init__(self, max_visitors, min_visitors):
        self.max_visitors = max_visitors
        self.min_visitors = min_visitors
        self.linear = cmp.LinearColormap(
            [config.circle_colour_1, config.circle_colour_2],
            vmin=self.min_visitors, vmax=self.max_visitors,
            caption='Visitors over 50 days'
        )

    def calculate_colour(self, visitors):
        return self.linear.rgba_hex_str(visitors)

    def calculate_size(self, visitors):
        scale = visitors / (self.max_visitors - self.min_visitors)
        radius = ((config.max_circle_radius - config.min_circle_radius) * scale) + config.min_circle_radius
        return radius


if __name__ == '__main__':
    generate_cycle_network(51.550267, 51.453854, -0.00083, -0.238211)
    # generate_main_roads_network(51.550267, 51.453854, -0.00083, -0.238211)

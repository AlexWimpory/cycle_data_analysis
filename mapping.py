import math

import folium
import webbrowser
import osmnx as ox
import networkx as nx
import branca.colormap as cmp


# TODO No path exception
# TODO Generate network based on long,lat box
# TODO find node based on long, lat allowing for shortest distance between stations
# TODO Logging

# Lat
# 51.549369
# 51.454752
# Long
# -0.002275
# -0.236769

class Map:
    def __init__(self, center, zoom_start, scale_generator):
        self.center = center
        self.zoom_start = zoom_start
        # Create map
        self.map = folium.Map(location=self.center, zoom_start=self.zoom_start)
        self.scale_generator = scale_generator

    def show_map(self):
        self.scale_generator.linear.add_to(self.map)
        folium.TileLayer('cartodbpositron').add_to(self.map)
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

    def generate_cycle_network(self):
        graph_data = ox.graph_from_point(self.center, dist=750, network_type="bike", retain_all=True)
        ox.save_graphml(graph_data, "data/network.graphml")

    def plot_network(self):
        graph_data = ox.load_graphml("data/network.graphml")
        ox.plot_graph_folium(graph_data, self.map, popup_attribute="name", weight=2, color="#8b0000")

    def plot_shortest_cycle_route(self):
        graph_data = ox.load_graphml("data/network.graphml")
        origin_node = list(graph_data.nodes())[0]
        destination_node = list(graph_data.nodes())[30]
        route = nx.shortest_path(graph_data, origin_node, destination_node)
        ox.plot_route_folium(graph_data, route, self.map, weight=10)


class ScaleGenerator:
    def __init__(self, max_visitors, min_visitors):
        self.max_visitors = max_visitors
        self.min_visitors = min_visitors
        self.linear = cmp.LinearColormap(
            ['yellow', 'red'],
            vmin=self.min_visitors, vmax=self.max_visitors,
            caption='Visitors over 50 days'  # Caption for Color scale or Legend
        )

    def calculate_colour(self, visitors):
        return self.linear.rgba_hex_str(visitors)

    def calculate_size(self, visitors):
        min_radius = 10
        max_radius = 150

        a = visitors / (self.max_visitors - self.min_visitors)
        b = ((max_radius - min_radius) * a) + min_radius

        return b


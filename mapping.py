import folium
import webbrowser
import osmnx as ox
import networkx as nx


# TODO No path exception
# TODO Generate network based on long,lat box
# TODO Use long,lat to find center
# TODO find node based on long, lat allowing for shortest distance between stations
# TODO Station use scale colour

# Lat
# 51.549369
# 51.454752
# Long
# -0.002275
# -0.236769

class Map:
    def __init__(self, center, zoom_start):
        self.center = center
        self.zoom_start = zoom_start
        # Create map
        self.map = folium.Map(location=self.center, zoom_start=self.zoom_start)

    def show_map(self):
        # Display the map
        self.map.save("map.html")
        webbrowser.open("map.html")

    def add_station(self, location, name):
        """
        Add a marker onto the map
        :param location: tuple containing longitude and latitude
        :param name: string for popup
        """
        folium.Circle(
            radius=100,
            location=location,
            popup=name,
            color="crimson",
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


if __name__ == '__main__':
    # Define coordinates of where we want to center our map
    cords = (51.5072, -0.1276)
    bike_map = Map(cords, 10)
    bike_map.add_station((51.529163, -0.10997), "River Street , Clerkenwell")
    bike_map.plot_shortest_cycle_route()
    bike_map.show_map()

import folium
import webbrowser


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


# Define coordinates of where we want to center our map
cords = [51.5072, -0.1276]
bike_map = Map(center=cords, zoom_start=10)
bike_map.add_station((51.529163, -0.10997), "River Street , Clerkenwell")
bike_map.show_map()

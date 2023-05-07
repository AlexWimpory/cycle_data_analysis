import pandas as pd


class Loader:
    def __init__(self, journey_path, weather_path, station_path):
        self.journeys = self.load_journeys(journey_path)
        self.daily = self.generate_daily(weather_path)
        self.locations = self.load_locations(station_path)
        self.routes = self.generate_route()

    @staticmethod
    def load_journeys(path):
        """
        Load the journey data and combine date/time columns to a datetime
        """
        print(f"Processing {path}")
        # Read csv and convert end date/time columns to str so that they can be converted to a datetime
        journey_df = pd.read_csv(path, dtype={'End Year': 'str', 'End Month': 'str', 'End Date': 'str',
                                              'End Hour': 'str', 'End Minute': 'str', 'Start Year': 'str',
                                              'Start Month': 'str', 'Start Date': 'str', 'Start Hour': 'str',
                                              'Start Minute': 'str'})
        # Convert to datetime and remove extra columns
        journey_df["end"] = pd.to_datetime(journey_df["End Year"] + journey_df["End Month"] + journey_df["End Date"]
                                           + " " + journey_df["End Hour"] + journey_df["End Minute"],
                                           format="%y%m%d %H%M")
        journey_df = journey_df.drop(["End Year", "End Month", "End Date", "End Hour", "End Minute"], axis=1)
        # Repeat for start columns
        journey_df["start"] = pd.to_datetime(
            journey_df["Start Year"] + journey_df["Start Month"] + journey_df["Start Date"]
            + " " + journey_df["Start Hour"] + journey_df["Start Minute"],
            format="%y%m%d %H%M")
        journey_df = journey_df.drop(["Start Year", "Start Month", "Start Date", "Start Hour", "Start Minute"], axis=1)
        return journey_df

    def generate_daily(self, path):
        """
        Load weather data and add total visitors per day column
        """
        print(f"Processing {path}")
        # Calculate total visitors per day from journey data and convert from series to dataframe
        daily_journey_df = self.journeys.groupby([self.journeys['start'].dt.date]).size().to_frame().reset_index()
        daily_journey_df["start"] = pd.to_datetime(daily_journey_df["start"])
        daily_journey_df.rename(columns={0: 'JOURNEYS'}, inplace=True)
        # Load weather data
        daily_df = pd.read_csv(path)
        daily_df["start"] = pd.to_datetime(daily_df["DATE"], format="%d/%m/%Y")
        daily_df.reset_index()
        # Merge dataframes
        daily_df = pd.merge(daily_journey_df, daily_df, how="outer", on="start")
        daily_df = daily_df.drop(["DATE", "LATITUDE", "LONGITUDE"], axis=1)
        return daily_df

    def load_locations(self, path):
        """
        Load the station data and add a column for coordinates and visitors
        """
        print(f"Processing {path}")
        location_df = pd.read_csv(path)
        # Combine lat and long into a single tuple column
        location_df['Coordinates'] = list(zip(location_df.Latitude, location_df.Longitude))
        # Add a column which contains the total visitors at each location over 50 days
        start_location_visitors = self.journeys.groupby('Start Station ID').size()
        end_location_visitors = self.journeys.groupby('End Station ID').size()
        total_location_visitors = start_location_visitors.add(end_location_visitors).to_frame().reset_index()
        total_location_visitors.rename(columns={"Start Station ID": 'Station ID', 0: "Visitors"}, inplace=True)
        location_df = pd.merge(location_df, total_location_visitors, how="outer", on="Station ID")
        # Missing location data for station ID 147,201,300,461,551,565,705,783 -> a bit alarming as these locations
        # exist due to there being visitors but the location is unknown
        return location_df

    def calculate_max_min_visitors(self):
        """
        Return the max and min of the visitors column
        """
        max_visitors = self.locations["Visitors"].max()
        min_visitors = self.locations["Visitors"].min()
        return max_visitors, min_visitors

    def generate_route(self):
        filtered = self.journeys.query('`Start Station ID` != `End Station ID`')
        return filtered.groupby(['Start Station ID', 'End Station ID']).size()

    def calculate_common_routes(self, num):
        common = self.routes.nlargest(n=num, keep="all").to_frame().reset_index()
        common["Start Cords"] = common["Start Station ID"].apply(self.find_station_cords)
        common["End Cords"] = common["End Station ID"].apply(self.find_station_cords)
        return common

    def find_station_cords(self, station_id):
        row = self.locations.loc[self.locations['Station ID'] == station_id]
        return row.iloc[0]["Longitude"], row.iloc[0]["Latitude"]


if __name__ == '__main__':
    data = Loader("data/bike_journeys.csv", "data/weather.csv", "data/bike_stations.csv")
    print(data.locations["Latitude"].max())
    print(data.locations["Latitude"].min())
    print(data.locations["Longitude"].max())
    print(data.locations["Longitude"].min())

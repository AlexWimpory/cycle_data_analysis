import pandas as pd
import matplotlib.pyplot as plt


class Loader:
    def __init__(self, journey_path, weather_path, station_path):
        self.journeys = self.load_journeys(journey_path)
        self.daily = self.generate_daily(weather_path)
        self.locations = self.load_locations(station_path)

    @staticmethod
    def load_journeys(path):
        # journey_df = pd.read_csv(path, parse_dates={"end": ["End Year", "End Month", "End Date"]})
        journey_df = pd.read_csv(path,
                                 dtype={'End Year': 'str', 'End Month': 'str', 'End Date': 'str',
                                        'End Hour': 'str', 'End Minute': 'str',
                                        'Start Year': 'str',
                                        'Start Month': 'str', 'Start Date': 'str',
                                        'Start Hour': 'str', 'Start Minute': 'str'})

        journey_df["end"] = pd.to_datetime(journey_df["End Year"] + journey_df["End Month"] + journey_df["End Date"]
                                           + " " + journey_df["End Hour"] + journey_df["End Minute"],
                                           format="%y%m%d %H%M")
        journey_df = journey_df.drop(["End Year", "End Month", "End Date", "End Hour", "End Minute"], axis=1)

        journey_df["start"] = pd.to_datetime(
            journey_df["Start Year"] + journey_df["Start Month"] + journey_df["Start Date"]
            + " " + journey_df["Start Hour"] + journey_df["Start Minute"],
            format="%y%m%d %H%M")
        journey_df = journey_df.drop(["Start Year", "Start Month", "Start Date", "Start Hour", "Start Minute"], axis=1)

        return journey_df

    def generate_daily(self, path):
        daily_journey_df = self.journeys.groupby([self.journeys['start'].dt.date]).size().to_frame().reset_index()
        daily_journey_df["start"] = pd.to_datetime(daily_journey_df["start"])
        daily_journey_df.rename(columns={0: 'JOURNEYS'}, inplace=True)

        daily_df = pd.read_csv(path)
        daily_df["start"] = pd.to_datetime(daily_df["DATE"], format="%d/%m/%Y")
        daily_df.reset_index()

        daily_df = pd.merge(daily_journey_df, daily_df, how="outer", on="start")
        return daily_df

    @staticmethod
    def load_locations(path):
        location_df = pd.read_csv(path)
        location_df['Coordinates'] = list(zip(location_df.Latitude, location_df.Longitude))
        return location_df


if __name__ == '__main__':
    data = Loader("data/bike_journeys.csv", "data/weather.csv", "data/bike_stations.csv")
    plt.scatter(data.daily["TAVG (CELSIUS)"], data.daily["JOURNEYS"])
    # plt.xlim(10, 24)
    # plt.ylim(15000, 45000)
    plt.show()

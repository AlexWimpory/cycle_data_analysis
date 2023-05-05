import pandas as pd
import matplotlib.pyplot as plt


class Loader:
    def __init__(self):
        self.journeys = self.load_journeys()
        self.daily = self.generate_daily()

    @staticmethod
    def load_journeys():
        journey_df = pd.read_csv('data/bike_journeys.csv',
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

    def generate_daily(self):
        daily_journey_df = self.journeys.groupby([self.journeys['start'].dt.date]).size().to_frame().reset_index()
        daily_journey_df["start"] = pd.to_datetime(daily_journey_df["start"])
        daily_journey_df.rename(columns={0: 'JOURNEYS'}, inplace=True)

        daily_df = pd.read_csv('data/weather.csv')
        daily_df["start"] = pd.to_datetime(daily_df["DATE"], format="%d/%m/%Y")
        daily_df.reset_index()

        daily_df = pd.merge(daily_journey_df, daily_df, how="outer", on="start")
        return daily_df


if __name__ == '__main__':
    data = Loader()
    plt.scatter(data.daily["TAVG (CELSIUS)"], data.daily["JOURNEYS"])
    # plt.xlim(10, 24)
    # plt.ylim(15000, 45000)
    plt.show()

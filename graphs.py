import matplotlib.pyplot as plt
from utilities import quantile_test
from scipy import stats


def plot_temp_vs_journeys(data):
    df_filtered = quantile_test(data.daily, "TAVG (CELSIUS)")
    df_filtered = quantile_test(df_filtered, "JOURNEYS")
    slope, intercept, _, _, _ = stats.linregress(df_filtered["TAVG (CELSIUS)"], df_filtered["JOURNEYS"])
    best_fit = [slope * i + intercept for i in df_filtered["TAVG (CELSIUS)"]]
    plt.scatter(df_filtered["TAVG (CELSIUS)"], df_filtered["JOURNEYS"])
    plt.plot(df_filtered["TAVG (CELSIUS)"], best_fit, color="m")
    plt.title("Temperature vs Journeys")
    plt.xlabel("Average Temperature (°C)")
    plt.ylabel("Number of Journeys")
    plt.grid(color='#d9d9d9')
    plt.savefig('graphs/temp_vs_journeys.png')
    plt.show()


def plot_prcp_vs_journeys(data):
    fig = plt.figure(figsize=(15,6))

    # Creating multiple axis for different scales
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    width = 0.4

    data.daily["PRCP (MM)"].plot(kind='bar', color='blue', ax=ax, width=width, position=1)
    data.daily["JOURNEYS"].plot(kind='bar', color='lightseagreen', ax=ax2, width=width, position=0)
    # Formatting
    ax.set_ylabel('Precipitation (MM)', color="blue")
    ax.set_xlabel('Day')
    ax2.set_ylabel('Number of Journeys', color="lightseagreen")
    ax.legend()
    ax2.legend(bbox_to_anchor=(1, 0.93))
    plt.title("Rainfall vs Journeys")

    plt.savefig('graphs/prcp_vs_journeys.png')
    plt.show()

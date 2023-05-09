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

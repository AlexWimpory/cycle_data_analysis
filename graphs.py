import matplotlib as plt


def plot_visitors_vs_temp(data):
    plt.scatter(data.daily["TAVG (CELSIUS)"], data.daily["JOURNEYS"])
    plt.show()

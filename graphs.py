import matplotlib.pyplot as plt


def plot_temp_vs_journeys(data):
    plt.scatter(data.daily["TAVG (CELSIUS)"], data.daily["JOURNEYS"])
    plt.title("Temperature vs Journeys")
    plt.xlabel("Average Temperature (°C)")
    plt.ylabel("Number of Journeys")
    plt.grid(color='#d9d9d9')
    plt.savefig('graphs/temp_vs_journeys.png')
    plt.show()

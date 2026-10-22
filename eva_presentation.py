"""Inherited country text and pyplot output blocks."""


def display_country_total(selected_country, country_hours):
    print(f"Total EVA duration for {selected_country}: {country_hours:.2f} hours")


def plot_cumulative_duration(dates, cumulative_hours):
    import matplotlib.pyplot as plt

    plt.plot(dates, cumulative_hours)
    plt.xlabel("Year")
    plt.ylabel("Cumulative EVA duration (hours)")
    plt.tight_layout()
    plt.savefig("cumulative_duration.png")
    plt.show()

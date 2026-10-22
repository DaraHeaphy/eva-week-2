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


def display_comparison(result):
    print(f"EVA comparison: {result['start_year']}-{result['end_year']} (inclusive)")
    for summary in (result["first"], result["second"]):
        average = ("unavailable" if summary["average_hours"] is None
                   else f"{summary['average_hours']:.2f} hours")
        print(f"{summary['country']}: {summary['count']} EVAs; "
              f"total {summary['total_hours']:.2f} hours; average {average}")
    print("Tie: equal total EVA duration" if result["winner"] is None
          else f"Greater total EVA duration: {result['winner']}")
    print("Scope: dated dataset entries with durations, including zero-duration entries.")

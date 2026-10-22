"""Inherited EVA application: coordinate the extracted original responsibilities."""
from eva_loading import load_eva_data
from eva_preparation import prepare_records
from eva_analysis import cumulative_duration, total_duration_for_country
from eva_presentation import display_country_total, plot_cumulative_duration


def main():
    eva_data = load_eva_data()
    records = prepare_records(eva_data)
    dates, cumulative_hours = cumulative_duration(records)

    selected_country = input("Country: ").strip()
    country_hours = total_duration_for_country(records, selected_country)
    display_country_total(selected_country, country_hours)

    plot_cumulative_duration(dates, cumulative_hours)


if __name__ == "__main__":
    main()

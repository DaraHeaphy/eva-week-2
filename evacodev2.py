"""Inherited EVA application: coordinate the extracted original responsibilities."""
import argparse
import sys

from eva_loading import load_eva_data
from eva_preparation import prepare_records
from eva_analysis import compare_countries, cumulative_duration, total_duration_for_country
from eva_presentation import display_comparison, display_country_total, plot_cumulative_duration


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inherited EVA analysis and country comparison")
    parser.add_argument("--compare", nargs=2, metavar=("COUNTRY_A", "COUNTRY_B"))
    parser.add_argument("--start-year", type=int)
    parser.add_argument("--end-year", type=int)
    args = parser.parse_args(argv)
    if not args.compare and (args.start_year is not None or args.end_year is not None):
        parser.error("Year options require --compare")

    eva_data = load_eva_data()
    records = prepare_records(eva_data)
    if args.compare:
        try:
            result = compare_countries(records, *args.compare, args.start_year, args.end_year)
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 2
        display_comparison(result)
        return 0

    dates, cumulative_hours = cumulative_duration(records)

    selected_country = input("Country: ").strip()
    country_hours = total_duration_for_country(records, selected_country)
    display_country_total(selected_country, country_hours)

    plot_cumulative_duration(dates, cumulative_hours)


if __name__ == "__main__":
    raise SystemExit(main())

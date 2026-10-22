"""Inherited numeric operations extracted without file, input or display effects."""


def cumulative_duration(records):
    """Accept chronological (date, duration_hours, country) tuples."""
    dates = []
    cumulative_hours = []
    total_hours = 0

    for date, duration_hours, country in records:
        total_hours += duration_hours
        dates.append(date)
        cumulative_hours.append(total_hours)
    return dates, cumulative_hours


def total_duration_for_country(records, selected_country):
    country_hours = sum(hours for _, hours, country in records if country.lower() == selected_country.lower())
    return country_hours

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


def _country_summary(records, selected_country):
    count = sum(1 for _, _, country in records
                if country.lower() == selected_country.lower())
    total_hours = total_duration_for_country(records, selected_country)
    return {"country": selected_country, "count": count, "total_hours": total_hours,
            "average_hours": total_hours / count if count else None}


def compare_countries(records, country_a, country_b, start_year, end_year):
    """Compare retained dataset entries over inclusive years; raise on invalid input."""
    from math import isclose

    if (type(start_year) is not int or type(end_year) is not int
            or not 1 <= start_year <= end_year <= 9999):
        raise ValueError("Use integer years with 1 <= start year <= end year <= 9999")
    known_countries = {country.lower(): country for _, _, country in records
                       if isinstance(country, str)}
    countries = []
    for country in (country_a, country_b):
        key = country.strip().lower() if isinstance(country, str) else ""
        if not key or key not in known_countries:
            available = ", ".join(sorted(known_countries.values())) or "none"
            raise ValueError(f"Unknown country: {country!r}. Available: {available}")
        countries.append(known_countries[key])

    period_records = [record for record in records if start_year <= record[0].year <= end_year]
    first = _country_summary(period_records, countries[0])
    second = _country_summary(period_records, countries[1])
    if isclose(first["total_hours"], second["total_hours"], rel_tol=0, abs_tol=1e-9):
        winner = None
    else:
        winner = first["country"] if first["total_hours"] > second["total_hours"] else second["country"]
    return {"first": first, "second": second, "start_year": start_year,
            "end_year": end_year, "winner": winner}

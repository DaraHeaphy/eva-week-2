import json
from datetime import datetime
import matplotlib.pyplot as plt

with open("eva-data.json", "r", encoding="utf-8") as file:
    eva_data = json.load(file)

records = []

for eva in eva_data:
    date_text = eva.get("date")
    duration_text = eva.get("duration")

    if not date_text or not duration_text:
        continue

    date = datetime.fromisoformat(date_text)
    hours, minutes = map(int, duration_text.split(":"))
    duration_hours = hours + minutes / 60

    records.append((date, duration_hours, eva.get("country")))

records.sort(key=lambda record: record[0])

dates = []
cumulative_hours = []
total_hours = 0

for date, duration_hours, country in records:
    total_hours += duration_hours
    dates.append(date)
    cumulative_hours.append(total_hours)

selected_country = input("Country: ").strip()
country_hours = sum(hours for _, hours, country in records if country.lower() == selected_country.lower())
print(f"Total EVA duration for {selected_country}: {country_hours:.2f} hours")

plt.plot(dates, cumulative_hours)
plt.xlabel("Year")
plt.ylabel("Cumulative EVA duration (hours)")
plt.tight_layout()
plt.savefig("cumulative_duration.png")
plt.show()

"""File-reading block extracted from the inherited evacodev2.py."""
import json


def load_eva_data(filename="eva-data.json"):
    with open(filename, "r", encoding="utf-8") as file:
        eva_data = json.load(file)
    return eva_data

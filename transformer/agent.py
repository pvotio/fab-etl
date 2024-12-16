import datetime
import json
import os

import pandas as pd


def get_columns():
    path = os.path.join(os.path.dirname(__file__), "columns.json")
    columns = json.load(open(path, "r"))
    return columns


def transform(parsed_data):
    df = pd.DataFrame(parsed_data)
    df["timestamp_created_utc"] = datetime.datetime.utcnow()
    if df.empty:
        raise ValueError("Dataframe is empty. Insertion terminated.")

    df = df.reindex(columns=get_columns())
    return df

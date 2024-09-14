import datetime

import pandas as pd


def transform(parsed_data):
    df = pd.DataFrame(parsed_data)
    df["timestamp_created_utc"] = datetime.datetime.utcnow()
    if df.empty:
        raise ValueError("Dataframe is empty. Insertion terminated.")
    return df

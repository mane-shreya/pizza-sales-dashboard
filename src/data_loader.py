import pandas as pd

def load_pizza_data():
    df = pd.read_csv("data/pizza_sales.csv")

    # Fix date format (DD-MM-YYYY)
    df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True)

    # Fix time format (11.38.36 → 11:38:36)
    df["order_time"] = pd.to_datetime(
        df["order_time"].astype(str).str.replace(".", ":", regex=False),
        errors="coerce"
    ).dt.time

    return df

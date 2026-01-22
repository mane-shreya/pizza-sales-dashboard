def total_revenue(df):
    return round(df["total_price"].sum(), 2)

def total_orders(df):
    return df["order_id"].nunique()

def total_pizzas_sold(df):
    return df["quantity"].sum()

def avg_order_value(df):
    return round(df["total_price"].sum() / df["order_id"].nunique(), 2)

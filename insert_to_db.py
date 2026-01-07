import psycopg2
import pandas as pd
from psycopg2.extras import execute_batch
import numpy
conn = psycopg2.connect(
    host="localhost",
    database="sql_project",
    user="postgres",
    password="Admin121"
)

cur = conn.cursor()

def insert_csv(path, table, columns):
    df = pd.read_csv(path)

    values = []
    for row in df[columns].to_numpy():
        clean_row = []
        for v in row:
            if pd.isna(v):
                clean_row.append(None)
            elif hasattr(v, "item"):
                clean_row.append(v.item())
            else:
                clean_row.append(v)
        values.append(tuple(clean_row))

    cols = ",".join(columns)
    query = f"""
        INSERT INTO bookstore.{table} ({cols})
        VALUES ({','.join(['%s'] * len(columns))})
    """

    execute_batch(cur, query, values, page_size=500)
    conn.commit()

    print(f"{table} inserted ({len(values)})")


insert_csv(
    "data/processed/categories.csv",
    "categories",
    ["category_id", "name"]
)

insert_csv(
    "data/processed/products.csv",
    "products",
    ["product_id", "name", "price", "category_id"]
)

insert_csv(
    "data/processed/customers.csv",
    "customers",
    ["customer_id", "name", "email", "city", "registration_date"]
)

insert_csv(
    "data/processed/orders.csv",
    "orders",
    ["order_id", "customer_id", "order_date", "total_amount"]
)

insert_csv(
    "data/processed/order_items.csv",
    "order_items",
    ["item_id", "order_id", "product_id", "quantity", "price"]
)

cur.close()
conn.close()

print("All data exported to PostgreSQL ")

# scripts/clean_and_generate.py

import pandas as pd
import os
from faker import Faker
import random
from datetime import datetime

fake = Faker()
os.makedirs('data/processed', exist_ok=True)

print("starting cleaning and fake data generation...")

# 1. Categories → CSV
cat_df = pd.read_json('data/raw/categories.json')
cat_df.to_csv('data/processed/categories.csv', index=False)
print("categories.csv saved")

# 2. Products → CSV
prod_df = pd.read_json('data/raw/products.json')
prod_df['price'] = prod_df['price'].astype(float)
prod_df = prod_df.drop_duplicates(subset=['name'])
prod_df.to_csv('data/processed/products.csv', index=False)
print(f"products.csv saved ({len(prod_df)} boook)")

# 3. Fake Customers
customers = []
for i in range(1, 1001):
    customers.append({
        'customer_id': i,
        'name': fake.name(),
        'email': fake.unique.email(),
        'city': fake.city(),
        'registration_date': fake.date_between(
            start_date='-5y',
            end_date=datetime.now().date()
        )
    })

pd.DataFrame(customers).to_csv('data/processed/customers.csv', index=False)
print("customers.csv saved (1000 customer)")

# 4. Fake Orders
orders = []
for i in range(1, 2501):
    orders.append({
        'order_id': i,
        'customer_id': random.randint(1, 1000),
        'order_date': fake.date_time_between(
            start_date='-5y',
            end_date=datetime.now()
        ),
        'total_amount': round(random.uniform(15, 400), 2)
    })

pd.DataFrame(orders).to_csv('data/processed/orders.csv', index=False)
print("orders.csv saved (2500 orders)")

# 5. Fake Order Items
order_items = []
item_id = 1

for order_id in range(1, 2501):
    num_items = random.randint(1, 6)
    for _ in range(num_items):
        product = prod_df.sample(1).iloc[0]
        quantity = random.randint(1, 5)
        price = round(product['price'] * quantity, 2)

        order_items.append({
            'item_id': item_id,
            'order_id': order_id,
            'product_id': product['product_id'],
            'quantity': quantity,
            'price': price
        })
        item_id += 1

pd.DataFrame(order_items).to_csv('data/processed/order_items.csv', index=False)
print(f"order_items.csv saved ({len(order_items)} row)")

print("Done!")

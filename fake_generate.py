import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()
os.makedirs('data/processed', exist_ok=True)

# Load products for referencing
products_df = pd.read_csv('data/processed/products.csv')

# Generate customers
customers = []
for i in range(1, 1001):
    customers.append({
        'customer_id': i,
        'name': fake.name(),
        'email': fake.email(),
        'city': fake.city(),
        'registration_date': fake.date_between(start_date='-5y', end_date='today')
    })
customers_df = pd.DataFrame(customers)
customers_df.to_csv('data/processed/customers.csv', index=False)

# Generate orders
orders = []
for i in range(1, 2001):
    order_date = fake.date_time_between(start_date='-5y', end_date='today')
    total_amount = round(random.uniform(10, 500), 2)
    orders.append({
        'order_id': i,
        'customer_id': random.randint(1, 1000),
        'order_date': order_date,
        'total_amount': total_amount
    })
orders_df = pd.DataFrame(orders)
orders_df.to_csv('data/processed/orders.csv', index=False)

# Generate order_items (3-5 items per order)
order_items = []
item_id = 1
for order_id in range(1, 2001):
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        product = products_df.sample(1).iloc[0]
        quantity = random.randint(1, 5)
        price = product['price'] * quantity
        order_items.append({
            'item_id': item_id,
            'order_id': order_id,
            'product_id': product['product_id'],
            'quantity': quantity,
            'price': price
        })
        item_id += 1
order_items_df = pd.DataFrame(order_items)
order_items_df.to_csv('data/processed/order_items.csv', index=False)

print("Fake data generated")
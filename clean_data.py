import pandas as pd
import os

os.makedirs('data/processed', exist_ok=True)

# Categories
categories_df = pd.read_json('data/raw/categories.json')
categories_df = categories_df.drop_duplicates(subset=['name'])  # No duplicates expected
categories_df.to_csv('data/processed/categories.csv', index=False)

# Products
products_df = pd.read_json('data/raw/products.json')
products_df['price'] = products_df['price'].astype(float)
products_df = products_df.drop_duplicates(subset=['name'])
products_df.to_csv('data/processed/products.csv', index=False)

print("Processed files saved")
import pandas as pd
from faker import Faker
import random
import os

fake = Faker()
random.seed(42)
Faker.seed(42)

NUM_CUSTOMERS = 1000
NUM_PRODUCTS  = 100
NUM_ORDERS    = 5000

CATEGORIES = ["Electronics", "Clothing", "Books", "Home & Kitchen", "Sports"]
STATUSES   = ["completed", "pending", "cancelled", "refunded"]

def generate_customers(n):
    customers = []
    for i in range(1, n + 1):
        customers.append({
            "customer_id": i,
            "name"       : fake.name(),
            "email"      : fake.email(),
            "city"       : fake.city(),
            "state"      : fake.state(),
            "signup_date": fake.date_between(start_date="-3y", end_date="today")
        })
    return pd.DataFrame(customers)

def generate_products(n):
    products = []
    for i in range(1, n + 1):
        products.append({
            "product_id"  : i,
            "product_name": fake.catch_phrase(),
            "category"    : random.choice(CATEGORIES),
            "price"       : round(random.uniform(5.99, 499.99), 2),
            "stock"       : random.randint(0, 500)
        })
    return pd.DataFrame(products)

def generate_orders(n, num_customers, num_products):
    orders = []
    for i in range(1, n + 1):
        orders.append({
            "order_id"   : i,
            "customer_id": random.randint(1, num_customers),
            "product_id" : random.randint(1, num_products),
            "quantity"   : random.randint(1, 5),
            "order_date" : fake.date_between(start_date="-1y", end_date="today"),
            "status"     : random.choice(STATUSES)
        })
    return pd.DataFrame(orders)

def save_data():
    os.makedirs("data/raw", exist_ok=True)

    customers = generate_customers(NUM_CUSTOMERS)
    products  = generate_products(NUM_PRODUCTS)
    orders    = generate_orders(NUM_ORDERS, NUM_CUSTOMERS, NUM_PRODUCTS)

    customers.to_csv("data/raw/customers.csv", index=False)
    products.to_csv("data/raw/products.csv",   index=False)
    orders.to_csv("data/raw/orders.csv",       index=False)

    print(f"✅ Customers : {len(customers)} rows → data/raw/customers.csv")
    print(f"✅ Products  : {len(products)} rows → data/raw/products.csv")
    print(f"✅ Orders    : {len(orders)} rows → data/raw/orders.csv")
    print("\n🎉 Raw data generated successfully!")

if __name__ == "__main__":
    save_data()

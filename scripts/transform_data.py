import pandas as pd
import os

def load_raw_data():
    customers = pd.read_csv("data/raw/customers.csv")
    products  = pd.read_csv("data/raw/products.csv")
    orders    = pd.read_csv("data/raw/orders.csv")
    return customers, products, orders

def transform(customers, products, orders):

    # ── 1. FIX DATA TYPES ───────────────────────────
    orders["order_date"]      = pd.to_datetime(orders["order_date"])
    customers["signup_date"]  = pd.to_datetime(customers["signup_date"])
    products["price"]         = products["price"].astype(float)

    # ── 2. CHECK FOR NULLS ──────────────────────────
    print("Nulls in customers:", customers.isnull().sum().sum())
    print("Nulls in products :", products.isnull().sum().sum())
    print("Nulls in orders   :", orders.isnull().sum().sum())

    # ── 3. REMOVE DUPLICATES ────────────────────────
    customers = customers.drop_duplicates()
    products  = products.drop_duplicates()
    orders    = orders.drop_duplicates()

    # ── 4. ADD TOTAL AMOUNT COLUMN ──────────────────
    orders = orders.merge(products[["product_id", "price"]], on="product_id", how="left")
    orders["total_amount"] = orders["quantity"] * orders["price"]
    orders = orders.drop(columns=["price"])

    # ── 5. JOIN ALL TABLES ──────────────────────────
    fact_orders = orders.merge(customers, on="customer_id", how="left")
    fact_orders = fact_orders.merge(products, on="product_id", how="left")

    # ── 6. ADD USEFUL COLUMNS ───────────────────────
    fact_orders["order_year"]  = fact_orders["order_date"].dt.year
    fact_orders["order_month"] = fact_orders["order_date"].dt.month

    return customers, products, orders, fact_orders

def save_processed(customers, products, orders, fact_orders):
    os.makedirs("data/processed", exist_ok=True)

    customers.to_csv("data/processed/customers_clean.csv",   index=False)
    products.to_csv("data/processed/products_clean.csv",     index=False)
    orders.to_csv("data/processed/orders_clean.csv",         index=False)
    fact_orders.to_csv("data/processed/fact_orders.csv",     index=False)

    print(f"\n✅ customers_clean : {len(customers)} rows")
    print(f"✅ products_clean  : {len(products)} rows")
    print(f"✅ orders_clean    : {len(orders)} rows")
    print(f"✅ fact_orders     : {len(fact_orders)} rows")
    print("\n🎉 Transform complete!")

if __name__ == "__main__":
    customers, products, orders = load_raw_data()
    customers, products, orders, fact_orders = transform(customers, products, orders)
    save_processed(customers, products, orders, fact_orders)

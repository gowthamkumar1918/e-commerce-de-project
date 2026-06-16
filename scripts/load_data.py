import pandas as pd
from sqlalchemy import create_engine, text

# ── 1. DATABASE CONNECTION ───────────────────────────
def get_engine():
    engine = create_engine("postgresql+psycopg2://gowthamkumarkoshika@localhost:5432/ecommerce_db")
    return engine

# ── 2. CREATE TABLES ────────────────────────────────
def create_tables(engine):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id  INT PRIMARY KEY,
                name         VARCHAR(100),
                email        VARCHAR(100),
                city         VARCHAR(100),
                state        VARCHAR(100),
                signup_date  DATE
            );
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS products (
                product_id   INT PRIMARY KEY,
                product_name VARCHAR(200),
                category     VARCHAR(100),
                price        FLOAT,
                stock        INT
            );
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id      INT PRIMARY KEY,
                customer_id   INT,
                product_id    INT,
                quantity      INT,
                order_date    DATE,
                status        VARCHAR(50),
                total_amount  FLOAT
            );
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fact_orders (
                order_id      INT,
                customer_id   INT,
                product_id    INT,
                quantity      INT,
                order_date    DATE,
                status        VARCHAR(50),
                total_amount  FLOAT,
                name          VARCHAR(100),
                email         VARCHAR(100),
                city          VARCHAR(100),
                state         VARCHAR(100),
                signup_date   DATE,
                product_name  VARCHAR(200),
                category      VARCHAR(100),
                price         FLOAT,
                stock         INT,
                order_year    INT,
                order_month   INT
            );
        """))

        conn.commit()
        print("✅ Tables created successfully!")

# ── 3. LOAD DATA ────────────────────────────────────
def load_data(engine):
    customers   = pd.read_csv("data/processed/customers_clean.csv")
    products    = pd.read_csv("data/processed/products_clean.csv")
    orders      = pd.read_csv("data/processed/orders_clean.csv")
    fact_orders = pd.read_csv("data/processed/fact_orders.csv")

    customers.to_sql("customers",   engine, if_exists="replace", index=False)
    products.to_sql("products",     engine, if_exists="replace", index=False)
    orders.to_sql("orders",         engine, if_exists="replace", index=False)
    fact_orders.to_sql("fact_orders", engine, if_exists="replace", index=False)

    print(f"✅ Loaded customers   : {len(customers)} rows")
    print(f"✅ Loaded products    : {len(products)} rows")
    print(f"✅ Loaded orders      : {len(orders)} rows")
    print(f"✅ Loaded fact_orders : {len(fact_orders)} rows")
    print("\n🎉 Load complete! Data is now in PostgreSQL!")

if __name__ == "__main__":
    engine = get_engine()
    create_tables(engine)
    load_data(engine)

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round as spark_round, year, month

# ── 1. START SPARK SESSION ──────────────────────────
spark = SparkSession.builder \
    .appName("EcommerceETL") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("✅ Spark Session started!")

# ── 2. READ RAW DATA ────────────────────────────────
customers = spark.read.csv("data/raw/customers.csv", header=True, inferSchema=True)
products  = spark.read.csv("data/raw/products.csv",  header=True, inferSchema=True)
orders    = spark.read.csv("data/raw/orders.csv",    header=True, inferSchema=True)

print(f"✅ Customers : {customers.count()} rows")
print(f"✅ Products  : {products.count()} rows")
print(f"✅ Orders    : {orders.count()} rows")

# ── 3. TRANSFORM ────────────────────────────────────
# Join orders with products to get price
orders_with_price = orders.join(products, on="product_id", how="left")

# Calculate total amount
orders_with_price = orders_with_price.withColumn(
    "total_amount", spark_round(col("quantity") * col("price"), 2)
)

# Join with customers
fact_orders = orders_with_price.join(customers, on="customer_id", how="left")

# Add year and month columns
fact_orders = fact_orders \
    .withColumn("order_year",  year(col("order_date"))) \
    .withColumn("order_month", month(col("order_date")))

print(f"✅ Fact Orders: {fact_orders.count()} rows")

# ── 4. SHOW SAMPLE ──────────────────────────────────
print("\n--- Sample Data ---")
fact_orders.select(
    "order_id", "name", "product_name", "category", "total_amount", "status"
).show(5)

# ── 5. ANALYTICS ────────────────────────────────────
print("--- Revenue by Category ---")
fact_orders.filter(col("status") == "completed") \
    .groupBy("category") \
    .sum("total_amount") \
    .orderBy("sum(total_amount)", ascending=False) \
    .show()

# ── 6. SAVE OUTPUT ──────────────────────────────────
fact_orders.write.mode("overwrite").parquet("data/processed/fact_orders_spark")
print("\n✅ Saved to parquet!")
print("\n🎉 PySpark ETL Complete!")

spark.stop()

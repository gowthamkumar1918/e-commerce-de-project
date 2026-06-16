# E-Commerce Data Pipeline & Analytics Warehouse

## Project Overview
An end-to-end ETL data pipeline that ingests raw e-commerce data, transforms it, and loads it into a PostgreSQL data warehouse for analytics.

## Tech Stack
- Python, Pandas, SQLAlchemy
- PostgreSQL
- Faker (data generation)
- Git & GitHub

## Pipeline Steps
1. Extract - Generated realistic e-commerce data (customers, products, orders)
2. Transform - Cleaned data, fixed types, calculated total_amount, joined tables
3. Load - Pushed to PostgreSQL with 4 analytics-ready tables

## Tables
- customers - 1000 rows
- products  - 100 rows
- orders    - 5000 rows
- fact_orders - 5000 rows

## How to Run
python3 scripts/generate_data.py
python3 scripts/transform_data.py
python3 scripts/load_data.py
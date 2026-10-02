# Automated Sales & Inventory Analytics

An end-to-end analytics automation project using Python, Pandas, SQLite, SQL and Power BI to transform raw sales and inventory data into validated analytical datasets and business dashboards.

## Tech Stack

- Python
- Pandas
- SQLite
- SQL
- Power BI

## Architecture

Raw CSV
→ Python ETL & Data Validation
→ Cleaned Data
→ SQLite Database
→ SQL Analytics
→ Power BI-ready CSVs
→ Power BI Dashboard

## Business Objective

Build a repeatable workflow to clean, validate and analyse retail sales and inventory data, while generating business-ready outputs for revenue, profit, product, category, regional and inventory analysis.

## Dataset

The project uses synthetic data created for analytics and data-quality testing.

- 50,050 raw sales records
- 50,000 clean sales transactions
- 500 products
- 5,000 customers
- 50 stores
- 500 inventory records
- 12 months of transaction history

The raw dataset intentionally contains duplicate records and missing values to demonstrate data-quality validation.

## Python ETL & Data Validation

The Python pipeline:

1. Reads raw CSV datasets using Pandas
2. Detects duplicate order IDs
3. Identifies missing discount values
4. Validates quantities and key IDs
5. Checks product, customer and store mappings
6. Removes duplicate sales records
7. Handles missing discount values
8. Cleans inventory data and calculates inventory value
9. Loads the validated datasets into SQLite
10. Generates an ETL audit log

### Validation Results

| Check | Before | After |
|---|---:|---:|
| Sales records | 50,050 | 50,000 |
| Duplicate order IDs | 50 | 0 |
| Missing discount values | 100 | 0 |
| Invalid quantities | 0 | 0 |
| Unmatched product IDs | 0 | 0 |
| Unmatched customer IDs | 0 | 0 |
| Unmatched store IDs | 0 | 0 |

## SQLite Database

The validated data is stored in SQLite using the following tables:

- `fact_sales`
- `dim_product`
- `dim_customer`
- `dim_store`
- `fact_inventory`

## SQL Analytics

SQL was used to generate analytical datasets and business insights using:

- JOINs
- GROUP BY
- CTEs
- CASE logic
- Window functions
- `LAG()` for month-over-month growth
- Ranking
- Aggregation
- Inventory-risk analysis

The SQL workflow generates:

- Monthly sales performance
- Category performance
- Regional performance
- Top products
- Inventory risk analysis

## Automation

The complete workflow can be executed using:

`run_project.bat`

The pipeline automatically:

1. Runs the Python ETL and validation process
2. Loads cleaned data into SQLite
3. Executes the analytical SQL queries
4. Generates Power BI-ready CSV datasets
5. Creates ETL and SQL execution logs

## Power BI Dashboard

The project includes a two-page Power BI dashboard covering:

### Executive Dashboard

- Total Revenue: ₹184.00M
- Total Profit: ₹44.45M
- Transactions: 50K
- Inventory Value: ₹55.80M
- Monthly revenue trends
- Category performance
- Regional performance
- Inventory status

### Product & Inventory Analysis

- Top products by revenue
- Top products by profit
- Product-level revenue and profit
- Units sold
- Category-level analysis

## Project Evidence

The repository includes verification material demonstrating the execution of the workflow:

- `Screenshots/etl_validation.png`
- `Screenshots/pipeline_execution.png`
- `Screenshots/sql_query_result.png`
- `Screenshots/database_row_count.png`
- `Screenshots/sql_window_function.png`
- `data/processed/etl_audit_log.csv`
- `data/processed/sql_execution_log.csv`

The Power BI folder contains both the `.pbix` project file and the exported dashboard PDF.

## How to Run

### Option 1 — Run complete pipeline

Double-click:

`run_project.bat`

### Option 2 — Run individual Python scripts

```bash
python python/etl_pipeline.py
python python/export_for_powerbi.py

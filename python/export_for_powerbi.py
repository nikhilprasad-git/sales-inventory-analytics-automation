import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DB = BASE / "sales_analytics.db"
OUT = BASE / "data" / "processed"

OUT.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB)

queries = {
    "monthly_sales.csv": """
        SELECT
            strftime('%Y-%m', order_date) AS month,
            ROUND(SUM(net_sales),2) AS revenue,
            ROUND(SUM(profit),2) AS profit,
            COUNT(*) AS transactions
        FROM fact_sales
        GROUP BY strftime('%Y-%m', order_date)
        ORDER BY month;
    """,

    "category_performance.csv": """
        SELECT
            p.category,
            ROUND(SUM(f.net_sales),2) AS revenue,
            ROUND(SUM(f.profit),2) AS profit,
            ROUND(
                SUM(f.profit) /
                NULLIF(SUM(f.net_sales),0) * 100,
                2
            ) AS margin_pct
        FROM fact_sales f
        JOIN dim_product p
            ON f.product_id = p.product_id
        GROUP BY p.category
        ORDER BY revenue DESC;
    """,

    "region_performance.csv": """
        SELECT
            s.region,
            ROUND(SUM(f.net_sales),2) AS revenue,
            ROUND(SUM(f.profit),2) AS profit,
            COUNT(DISTINCT f.order_id) AS transactions
        FROM fact_sales f
        JOIN dim_store s
            ON f.store_id = s.store_id
        GROUP BY s.region
        ORDER BY revenue DESC;
    """,

    "top_products.csv": """
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            ROUND(SUM(f.net_sales),2) AS revenue,
            ROUND(SUM(f.profit),2) AS profit,
            SUM(f.quantity) AS units_sold
        FROM fact_sales f
        JOIN dim_product p
            ON f.product_id = p.product_id
        GROUP BY
            p.product_id,
            p.product_name,
            p.category
        ORDER BY revenue DESC;
    """,

    "inventory_risk.csv": """
        SELECT
            stock_status,
            COUNT(*) AS sku_count,
            ROUND(SUM(inventory_value),2) AS inventory_value
        FROM fact_inventory
        GROUP BY stock_status
        ORDER BY inventory_value DESC;
    """
}


# -----------------------------------------
# SQL EXECUTION LOG
# -----------------------------------------

execution_log = []

print("=" * 60)
print("SQL ANALYTICS & POWER BI EXPORT")
print("=" * 60)

for filename, query in queries.items():

    query_name = filename.replace(".csv", "")

    try:
        start_time = datetime.now()

        df = pd.read_sql_query(query, conn)

        df.to_csv(OUT / filename, index=False)

        execution_time = datetime.now()

        execution_log.append({
            "run_timestamp": execution_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "query_name": query_name,
            "output_file": filename,
            "rows_returned": len(df),
            "status": "PASS"
        })

        print(
            f"PASS | {query_name:<25} | "
            f"{len(df):>5} rows | {filename}"
        )

    except Exception as e:

        execution_log.append({
            "run_timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "query_name": query_name,
            "output_file": filename,
            "rows_returned": 0,
            "status": f"FAIL: {str(e)}"
        })

        print(
            f"FAIL | {query_name:<25} | {str(e)}"
        )


# -----------------------------------------
# SAVE SQL EXECUTION LOG
# -----------------------------------------

log_df = pd.DataFrame(execution_log)

log_path = OUT / "sql_execution_log.csv"

log_df.to_csv(
    log_path,
    index=False
)

conn.close()

print("\n" + "=" * 60)
print("SQL EXECUTION SUMMARY")
print("=" * 60)

for _, row in log_df.iterrows():
    print(
        f"{row['status']:<5} | "
        f"{row['query_name']:<25} | "
        f"{row['rows_returned']} rows"
    )

print("\nSQL execution log created:")
print(log_path)

print("\n" + "=" * 60)
print("POWER BI DATASETS GENERATED SUCCESSFULLY")
print("=" * 60)
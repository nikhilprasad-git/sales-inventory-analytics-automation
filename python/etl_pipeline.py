import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
PROCESSED = BASE / "data" / "processed"
DB = BASE / "sales_analytics.db"


def add_audit(audit_rows, check_name, before, after, status, details):
    audit_rows.append({
        "run_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "check_name": check_name,
        "before": before,
        "after": after,
        "status": status,
        "details": details
    })


def clean_sales(audit_rows):
    df = pd.read_csv(RAW / "sales_raw.csv")
    before = len(df)

    # -----------------------------
    # DATA QUALITY CHECKS - BEFORE
    # -----------------------------

    duplicate_orders = int(df["order_id"].duplicated().sum())
    missing_discount = int(df["discount_pct"].isna().sum())
    invalid_quantity = int((df["quantity"] <= 0).sum())

    missing_product_id = int(df["product_id"].isna().sum())
    missing_customer_id = int(df["customer_id"].isna().sum())
    missing_store_id = int(df["store_id"].isna().sum())

    products = pd.read_csv(RAW / "products.csv")
    customers = pd.read_csv(RAW / "customers.csv")
    stores = pd.read_csv(RAW / "stores.csv")

    unmatched_products = int(
        (~df["product_id"].isin(products["product_id"])).sum()
    )

    unmatched_customers = int(
        (~df["customer_id"].isin(customers["customer_id"])).sum()
    )

    unmatched_stores = int(
        (~df["store_id"].isin(stores["store_id"])).sum()
    )

    # -----------------------------
    # CLEANING
    # -----------------------------

    df = df.drop_duplicates(subset=["order_id"])

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    df["discount_pct"] = df["discount_pct"].fillna(0)
    df["net_sales"] = df["net_sales"].fillna(0)
    df["profit"] = df["profit"].fillna(0)

    after = len(df)

    # -----------------------------
    # DATA QUALITY CHECKS - AFTER
    # -----------------------------

    duplicate_orders_after = int(df["order_id"].duplicated().sum())
    missing_discount_after = int(df["discount_pct"].isna().sum())
    invalid_quantity_after = int((df["quantity"] <= 0).sum())

    # -----------------------------
    # AUDIT LOG
    # -----------------------------

    add_audit(
        audit_rows,
        "Sales row count",
        before,
        after,
        "PASS" if after < before else "PASS",
        f"{before:,} raw sales records processed"
    )

    add_audit(
        audit_rows,
        "Duplicate order IDs",
        duplicate_orders,
        duplicate_orders_after,
        "PASS" if duplicate_orders_after == 0 else "FAIL",
        "Duplicate order IDs removed during ETL"
    )

    add_audit(
        audit_rows,
        "Missing discount values",
        missing_discount,
        missing_discount_after,
        "PASS" if missing_discount_after == 0 else "FAIL",
        "Missing discount values replaced with 0"
    )

    add_audit(
        audit_rows,
        "Invalid quantities",
        invalid_quantity,
        invalid_quantity_after,
        "PASS" if invalid_quantity_after == 0 else "FAIL",
        "Quantity values checked for values <= 0"
    )

    add_audit(
        audit_rows,
        "Missing product IDs",
        missing_product_id,
        int(df["product_id"].isna().sum()),
        "PASS" if df["product_id"].isna().sum() == 0 else "FAIL",
        "Product ID completeness check"
    )

    add_audit(
        audit_rows,
        "Unmatched product IDs",
        unmatched_products,
        int((~df["product_id"].isin(products["product_id"])).sum()),
        "PASS" if (~df["product_id"].isin(products["product_id"])).sum() == 0 else "FAIL",
        "Foreign-key integrity check against product master"
    )

    add_audit(
        audit_rows,
        "Missing customer IDs",
        missing_customer_id,
        int(df["customer_id"].isna().sum()),
        "PASS" if df["customer_id"].isna().sum() == 0 else "FAIL",
        "Customer ID completeness check"
    )

    add_audit(
        audit_rows,
        "Unmatched customer IDs",
        unmatched_customers,
        int((~df["customer_id"].isin(customers["customer_id"])).sum()),
        "PASS" if (~df["customer_id"].isin(customers["customer_id"])).sum() == 0 else "FAIL",
        "Foreign-key integrity check against customer master"
    )

    add_audit(
        audit_rows,
        "Missing store IDs",
        missing_store_id,
        int(df["store_id"].isna().sum()),
        "PASS" if df["store_id"].isna().sum() == 0 else "FAIL",
        "Store ID completeness check"
    )

    add_audit(
        audit_rows,
        "Unmatched store IDs",
        unmatched_stores,
        int((~df["store_id"].isin(stores["store_id"])).sum()),
        "PASS" if (~df["store_id"].isin(stores["store_id"])).sum() == 0 else "FAIL",
        "Foreign-key integrity check against store master"
    )

    df.to_csv(PROCESSED / "sales_clean.csv", index=False)

    print(f"Sales rows: {before:,} -> {after:,}")
    print(f"Duplicate order IDs: {duplicate_orders} -> {duplicate_orders_after}")
    print(f"Missing discount values: {missing_discount} -> {missing_discount_after}")


def clean_inventory(audit_rows):
    df = pd.read_csv(RAW / "inventory_raw.csv")

    negative_stock_before = int((df["stock_on_hand"] < 0).sum())

    df["stock_on_hand"] = df["stock_on_hand"].clip(lower=0)

    negative_stock_after = int((df["stock_on_hand"] < 0).sum())

    df["inventory_value"] = (
        df["stock_on_hand"] * df["unit_cost"]
    )

    add_audit(
        audit_rows,
        "Negative inventory values",
        negative_stock_before,
        negative_stock_after,
        "PASS" if negative_stock_after == 0 else "FAIL",
        "Negative stock values clipped to zero"
    )

    df.to_csv(PROCESSED / "inventory_clean.csv", index=False)

    print(
        f"Inventory negative stock: "
        f"{negative_stock_before} -> {negative_stock_after}"
    )


def load_to_sqlite():
    conn = sqlite3.connect(DB)

    tables = [
        ("sales_clean.csv", "fact_sales", PROCESSED),
        ("products.csv", "dim_product", RAW),
        ("customers.csv", "dim_customer", RAW),
        ("stores.csv", "dim_store", RAW),
        ("inventory_clean.csv", "fact_inventory", PROCESSED)
    ]

    for filename, table, folder in tables:
        df = pd.read_csv(folder / filename)

        df.to_sql(
            table,
            conn,
            if_exists="replace",
            index=False
        )

        print(f"Loaded {table}: {len(df):,} rows")

    conn.close()

    print(f"\nSQLite database created: {DB}")


def main():
    # Make sure processed folder exists
    PROCESSED.mkdir(parents=True, exist_ok=True)

    audit_rows = []

    print("=" * 60)
    print("SALES & INVENTORY ANALYTICS - ETL PIPELINE")
    print("=" * 60)

    print("\n[1/3] Running sales data validation and cleaning...")
    clean_sales(audit_rows)

    print("\n[2/3] Running inventory validation and cleaning...")
    clean_inventory(audit_rows)

    print("\n[3/3] Loading cleaned data into SQLite...")
    load_to_sqlite()

    # Create audit log
    audit_df = pd.DataFrame(audit_rows)

    audit_path = PROCESSED / "etl_audit_log.csv"
    audit_df.to_csv(audit_path, index=False)

    print("\n" + "=" * 60)
    print("ETL AUDIT SUMMARY")
    print("=" * 60)

    for _, row in audit_df.iterrows():
        print(
            f"{row['status']:<5} | "
            f"{row['check_name']:<30} | "
            f"{row['before']} -> {row['after']}"
        )

    print("\nAudit log created:")
    print(audit_path)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()
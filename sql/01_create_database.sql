CREATE DATABASE IF NOT EXISTS sales_analytics;
USE sales_analytics;

CREATE TABLE dim_product (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    unit_cost DECIMAL(12,2),
    unit_price DECIMAL(12,2)
);

CREATE TABLE dim_customer (
    customer_id VARCHAR(10) PRIMARY KEY,
    customer_name VARCHAR(100),
    segment VARCHAR(50),
    region VARCHAR(30)
);

CREATE TABLE dim_store (
    store_id VARCHAR(10) PRIMARY KEY,
    store_name VARCHAR(100),
    region VARCHAR(30),
    city VARCHAR(50)
);

CREATE TABLE fact_sales (
    order_id VARCHAR(20) PRIMARY KEY,
    order_date DATE,
    product_id VARCHAR(10),
    customer_id VARCHAR(10),
    store_id VARCHAR(10),
    quantity INT,
    unit_cost DECIMAL(12,2),
    unit_price DECIMAL(12,2),
    discount_pct DECIMAL(6,4),
    gross_sales DECIMAL(14,2),
    discount_amount DECIMAL(14,2),
    net_sales DECIMAL(14,2),
    cost DECIMAL(14,2),
    profit DECIMAL(14,2),
    margin_pct DECIMAL(8,4)
);

CREATE TABLE fact_inventory (
    product_id VARCHAR(10),
    category VARCHAR(50),
    unit_cost DECIMAL(12,2),
    unit_price DECIMAL(12,2),
    store_id VARCHAR(10),
    stock_on_hand INT,
    reorder_level INT,
    inventory_value DECIMAL(14,2),
    stock_status VARCHAR(20)
);

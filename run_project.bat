@echo off

echo ============================================================
echo SALES AND INVENTORY ANALYTICS PIPELINE
echo ============================================================

echo.
echo [1/2] Running Python ETL and data validation...
echo.

python python\etl_pipeline.py

if errorlevel 1 (
    echo.
    echo ETL PIPELINE FAILED.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo [2/2] Running SQL analytics and Power BI export...
echo ============================================================

python python\export_for_powerbi.py

if errorlevel 1 (
    echo.
    echo SQL EXPORT FAILED.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo COMPLETE PIPELINE FINISHED SUCCESSFULLY
echo ============================================================

echo.
echo Generated evidence:
echo - data\processed\etl_audit_log.csv
echo - data\processed\sql_execution_log.csv

echo.
echo Generated Power BI datasets:
echo - monthly_sales.csv
echo - category_performance.csv
echo - region_performance.csv
echo - top_products.csv
echo - inventory_risk.csv

echo.
pause
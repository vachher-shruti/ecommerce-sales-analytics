# E-commerce Sales Analytics

## Overview

This project analyses online retail transaction data to understand sales performance, product trends, and customer purchasing behaviour. The goal is to identify useful business insights through data cleaning, exploratory analysis, and data visualisation.

## Business Questions

- Which products generate the most revenue?
- How do sales change over time?
- Which countries contribute the most revenue?
- Who are the most valuable customers?
- What business opportunities can be identified from the data?

## Tools

- **Python:** Data cleaning, exploratory data analysis, and visualisation
- **SQL:** Querying and analysing sales data
- **Power BI:** Interactive dashboard development

## Dataset

Source: [UCI Machine Learning Repository — Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)

The dataset contains online retail transactions, including invoice numbers, product details, quantities, unit prices, invoice dates, customer IDs, and countries.

## Python Analysis Completed

- Inspected the dataset and checked for missing values and duplicate records.
- Removed exact duplicate rows.
- Investigated cancellations, negative quantities, unusual prices, and missing values.
- Created a filtered dataset for positive-value sales analysis.
- Analysed revenue by product, month, country, and customer.
- Generated charts for monthly revenue and top physical products.
- Exported the filtered dataset to CSV.

## Key Findings

- The filtered sales dataset contains **524,878 records**.
- Total positive-sales revenue in the filtered dataset is approximately **£10.64 million**.
- The Regency Cake Stand 3 Tier generated approximately **£174,156.54** in recorded sales revenue, ranking first among the physical products included in the analysis.
- November 2011 had the highest monthly revenue, at approximately **£1.50 million**.
- The United Kingdom contributed approximately **£9.00 million** in filtered sales revenue.

### Notes and Limitations

- Revenue represents positive-value sales after filtering, not net revenue after returns.
- December 2011 may be a partial month because the source dataset ends during December.
- The physical-product ranking excludes stock codes `DOT`, `POST`, and `M` based on the project's current classification assumption.

## Project Structure

```text
ecommerce-sales-analytics/
├── README.md
└── python/
    ├── sales_analysis_cleaned.py
    ├── analysis_summary.txt
    ├── monthly_revenue.png
    └── top_10_products.png

The cleaned dataset (`cleaned_sales_data.csv`) is generated locally by the Python script and is not included in the repository because of its file size.

## Next Steps

- Perform SQL-based sales analysis.
- Build an interactive Power BI dashboard.
- Develop additional business insights and recommendations.


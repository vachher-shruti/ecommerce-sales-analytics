"""E-commerce sales analysis using the UCI Online Retail dataset.

Place this script in the same folder as Online Retail.xlsx, then run:
    python sales_analysis_cleaned.py

Outputs:
    analysis_summary.txt
    monthly_revenue.png
    top_10_products.png
    cleaned_sales_data.csv
"""

import pandas as pd
import matplotlib.pyplot as plt


# 1. Load data ---------------------------------------------------------------
df = pd.read_excel("Online Retail.xlsx")

print("DATASET OVERVIEW")
print("Rows and columns:", df.shape)
print("Columns:", df.columns.tolist())


# 2. Inspect data quality ----------------------------------------------------
missing_values = df.isna().sum()
duplicate_count = int(df.duplicated().sum())

print("\nMISSING VALUES")
print(missing_values.to_string())
print("\nExact duplicate rows:", duplicate_count)

# Create a copy without exact duplicate rows.
clean_df = df.drop_duplicates().copy()

# Calculate line-level revenue. This is quantity multiplied by unit price.
clean_df["Revenue"] = clean_df["Quantity"] * clean_df["UnitPrice"]

is_cancelled = clean_df["InvoiceNo"].astype(str).str.startswith("C")
negative_quantity = clean_df["Quantity"] < 0

print("\nDATA-QUALITY INVESTIGATION")
print("Rows after removing exact duplicates:", len(clean_df))
print("Rows removed as exact duplicates:", len(df) - len(clean_df))
print("Cancellation rows (invoice number starts with C):", int(is_cancelled.sum()))
print("Rows with negative quantity:", int(negative_quantity.sum()))
print(
    "Negative-quantity rows without a C invoice prefix:",
    int((negative_quantity & ~is_cancelled).sum()),
)
print("Rows with zero unit price:", int((clean_df["UnitPrice"] == 0).sum()))
print("Rows with negative unit price:", int((clean_df["UnitPrice"] < 0).sum()))
print("Rows with missing CustomerID:", int(clean_df["CustomerID"].isna().sum()))
print("Rows with missing Description:", int(clean_df["Description"].isna().sum()))

# The raw total includes negative and zero-value records, so it is not the same
# metric as the positive-sales total calculated below.
raw_revenue = (df["Quantity"] * df["UnitPrice"]).sum()
print("\nRAW DATA REVENUE SUMMARY")
print("Revenue before filtering:", round(raw_revenue, 2))
print("Positive-revenue rows:", int(((df["Quantity"] * df["UnitPrice"]) > 0).sum()))
print("Negative-revenue rows:", int(((df["Quantity"] * df["UnitPrice"]) < 0).sum()))
print("Zero-revenue rows:", int(((df["Quantity"] * df["UnitPrice"]) == 0).sum()))


# 3. Prepare the sales-analysis dataset -------------------------------------
# This filter keeps ordinary positive-value sales for sales comparisons.
# It does not calculate net revenue after returns.
is_not_cancelled = ~clean_df["InvoiceNo"].astype(str).str.startswith("C")
is_positive_quantity = clean_df["Quantity"] > 0
is_positive_price = clean_df["UnitPrice"] > 0
has_description = clean_df["Description"].notna()

sales_df = clean_df[
    is_not_cancelled
    & is_positive_quantity
    & is_positive_price
    & has_description
].copy()
sales_df["Revenue"] = sales_df["Quantity"] * sales_df["UnitPrice"]

print("\nFILTERED SALES DATASET")
print("Rows retained:", len(sales_df))
print("Positive-sales revenue total:", round(sales_df["Revenue"].sum(), 2))
print("Unique invoices:", sales_df["InvoiceNo"].nunique())
print("Unique stock codes:", sales_df["StockCode"].nunique())


# 4. Analyse sales -----------------------------------------------------------
# Top 10 physical products by revenue.
# These codes are excluded based on the project's current classification
# assumption; review the assumption if the dataset suggests otherwise.
non_product_codes = ["DOT", "POST", "M"]
physical_products_df = sales_df[
    ~sales_df["StockCode"].astype(str).isin(non_product_codes)
].copy()

top_products = (
    physical_products_df.groupby(["StockCode", "Description"])["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Monthly revenue using filtered positive sales.
sales_df["Month"] = sales_df["InvoiceDate"].dt.to_period("M")
monthly_revenue = sales_df.groupby("Month")["Revenue"].sum().sort_index()

# Revenue by country.
country_sales = (
    sales_df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Customer ranking excludes rows where the customer ID is missing.
customer_sales = (
    sales_df.dropna(subset=["CustomerID"])
    .groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 PHYSICAL PRODUCTS BY REVENUE")
print(top_products.to_string())
print("\nTOP 10 MONTHS / MONTHLY REVENUE")
print(monthly_revenue.to_string())
print("\nTOP 10 COUNTRIES BY REVENUE")
print(country_sales.to_string())
print("\nTOP 10 CUSTOMERS BY REVENUE")
print(customer_sales.to_string())


# 5. Create charts -----------------------------------------------------------
ax = monthly_revenue.plot(kind="line", marker="o", figsize=(10, 5))
ax.set_title("Monthly Revenue Trend (Filtered Positive Sales)")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_revenue.png", dpi=300)
plt.close()

ax = top_products.sort_values().plot(kind="barh", figsize=(10, 6))
ax.set_title("Top 10 Physical Products by Revenue")
ax.set_xlabel("Revenue (£)")
ax.set_ylabel("Product")
plt.tight_layout()
plt.savefig("top_10_products.png", dpi=300)
plt.close()


# 6. Export cleaned data for Power BI ---------------------------------------
sales_df.to_csv("cleaned_sales_data.csv", index=False)
print("\nSaved cleaned_sales_data.csv, monthly_revenue.png, and top_10_products.png")


# 7. Write a summary report --------------------------------------------------
with open("analysis_summary.txt", "w", encoding="utf-8") as report:
    report.write("ONLINE RETAIL SALES ANALYSIS\n")
    report.write("============================\n\n")
    report.write("DATASET OVERVIEW\n")
    report.write(f"Original rows: {df.shape[0]}\n")
    report.write(f"Original columns: {df.shape[1]}\n")
    report.write(f"Exact duplicate rows: {duplicate_count}\n")
    report.write(f"Rows after removing duplicates: {len(clean_df)}\n")
    report.write(f"Missing CustomerIDs after deduplication: {clean_df['CustomerID'].isna().sum()}\n")
    report.write(f"Missing descriptions after deduplication: {clean_df['Description'].isna().sum()}\n")
    report.write(f"Raw revenue before filtering: {raw_revenue:.2f}\n\n")

    report.write("FILTERED SALES DATASET\n")
    report.write(f"Rows retained: {len(sales_df)}\n")
    report.write(f"Positive-sales revenue total: {sales_df['Revenue'].sum():.2f}\n")
    report.write(f"Unique invoices: {sales_df['InvoiceNo'].nunique()}\n")
    report.write(f"Unique stock codes: {sales_df['StockCode'].nunique()}\n\n")

    report.write("TOP 10 PHYSICAL PRODUCTS BY REVENUE\n")
    report.write(top_products.to_string())
    report.write("\n\nMONTHLY REVENUE (FILTERED POSITIVE SALES)\n")
    report.write(monthly_revenue.to_string())
    report.write("\n\nTOP 10 COUNTRIES BY REVENUE\n")
    report.write(country_sales.to_string())
    report.write("\n\nTOP 10 CUSTOMERS BY REVENUE\n")
    report.write(customer_sales.to_string())
    report.write("\n\nNOTES AND LIMITATIONS\n")
    report.write(
        "Revenue in the filtered sales dataset represents positive-value sales "
        "after the stated filters; it is not net revenue after returns.\n"
    )
    report.write(
        "December 2011 may be a partial month because the source dataset ends "
        "during December.\n"
    )
    report.write(
        "The physical-product ranking excludes stock codes DOT, POST, and M "
        "based on the project's current classification assumption.\n"
    )

print("Saved analysis_summary.txt")

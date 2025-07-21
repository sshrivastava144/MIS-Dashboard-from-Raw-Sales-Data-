import pandas as pd

# Step 1: Read the data
df = pd.read_csv('sales_data.csv', sep='\t')

# Step 2: Clean column names
df.columns = df.columns.str.strip()

# Step 3: Convert 'Order Date' to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

# Step 4: Drop rows with missing essential data
df = df.dropna(subset=['Order Date', 'Region', 'Salesperson', 'Product', 'Order Value'])

# Step 5: Cleaned data preview
print("✅ Cleaned Data (Top 5 Rows):\n")
print(df.head())

# Step 6: Add 'Month-Year' column
df['Month-Year'] = df['Order Date'].dt.to_period('M')

# Step 7: Month-on-Month Sales Trend
monthly_sales = df.groupby('Month-Year')['Order Value'].sum().sort_index()
print("\n Month-on-Month (MoM) Sales Trend:\n")
print(monthly_sales)

# Step 8: Top 5 Products by Sales
top_products = df.groupby('Product')['Order Value'].sum().nlargest(5)
print("\n Top 5 Products by Total Sales:\n")
print(top_products)

# Step 9: Region-wise Performance
region_sales = df.groupby('Region')['Order Value'].sum()
print("\n🌍 Region-wise Sales Performance:\n")
print(region_sales)

# Step 10: Salesperson-wise Performance
salesperson_sales = df.groupby('Salesperson')['Order Value'].sum()
print("\n🧑‍💼 Salesperson-wise Sales Performance:\n")
print(salesperson_sales)

# Step 11 (Optional): Save cleaned and processed data for Excel/BI Tool use
df.to_csv("cleaned_sales_data.csv", index=False)
print("\n Cleaned data saved as 'cleaned_sales_data.csv'")

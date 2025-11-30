import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Connect to DB
conn = psycopg2.connect(
    host="localhost",
    database="salesdb",
    user="rajatbaranwal",
    password=""
)

df = pd.read_sql("SELECT * FROM sales_data", conn)
conn.close()

df['timestamp'] = pd.to_datetime(df['timestamp'])
df['revenue'] = df['quantity'] * df['price']
df['date'] = df['timestamp'].dt.date

# =============================
# 1. Daily Revenue Trend
# =============================
daily_revenue = df.groupby('date')['revenue'].sum()

plt.figure(figsize=(10,5))
daily_revenue.plot(kind='line', marker='o')
plt.title("Daily Revenue Trend")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# =============================
# 2. Top Selling Products
# =============================
product_sales = df.groupby("product_name")['quantity'].sum()

plt.figure(figsize=(7,5))
product_sales.plot(kind='bar')
plt.title("Top Selling Products (Quantity)")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.tight_layout()
plt.show()

# =============================
# 3. Daily Quantity Trend
# =============================
daily_qty = df.groupby('date')['quantity'].sum()

plt.figure(figsize=(10,5))
daily_qty.plot(kind='line', color='green', marker='o')
plt.title("Daily Quantity Sold")
plt.xlabel("Date")
plt.ylabel("Quantity")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# =============================
# 4. Price Distribution
# =============================
plt.figure(figsize=(7,5))
plt.hist(df['price'], bins=20, color='orange')
plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

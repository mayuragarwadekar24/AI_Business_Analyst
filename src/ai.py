import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.stdout.reconfigure(encoding="utf-8")
# Force Ollama to use CPU
os.environ["OLLAMA_LLM_LIBRARY"] = os.getenv("OLLAMA_LLM_LIBRARY", "cpu")


import ollama
import psycopg
import pandas as pd

conn = psycopg.connect(
    host="localhost",
    dbname = "ai_business_analyst",
    user = "postgres",
    password = os.getenv("POSTGRES_PASSWORD"),
    port=5432
)



customers = pd.read_sql("SELECT * FROM customers", conn)
products = pd.read_sql("SELECT * FROM products", conn)
orders = pd.read_sql("SELECT * FROM orders", conn)

# Remove known invalid placeholder rows for AI analysis only

customers = customers[customers["customer_id"] != "customer_i"]

products = products[products["product_id"] != "product_id"]

orders = orders[orders["order_id"] != "order_id"]

print("Customers:", len(customers))
print("Products:", len(products))
print("Orders:", len(orders))


# Generate verified findings automatically

orders["order_date"] = pd.to_datetime(orders["order_date"])

# 1. Highest-selling category
category_sales = (
    orders.merge(products, on="product_id")
    .groupby("category")["sales"]
    .sum()
    .sort_values(ascending=False)
)

top_category = category_sales.index[0]
top_category_sales = category_sales.iloc[0]

# 2. Highest-selling product
product_sales = (
    orders.merge(products, on="product_id")
    .groupby("product_name")["sales"]
    .sum()
    .sort_values(ascending=False)
)

top_product = product_sales.index[0]
top_product_sales = product_sales.iloc[0]

# 3. Highest-selling brand
brand_sales = (
    orders.merge(products, on="product_id")
    .groupby("brand")["sales"]
    .sum()
    .sort_values(ascending=False)
)

top_brand = brand_sales.index[0]
top_brand_sales = brand_sales.iloc[0]

# 4. Highest-selling city
city_sales = (
    orders.merge(customers, on="customer_id")
    .groupby("city")["sales"]
    .sum()
    .sort_values(ascending=False)
)

top_city = city_sales.index[0]
top_city_sales = city_sales.iloc[0]

# 5 & 6. Highest and lowest sales month
monthly_sales = (
    orders.groupby(orders["order_date"].dt.month)["sales"]
    .sum()
    .sort_values(ascending=False)
)

highest_month = monthly_sales.index[0]
highest_month_sales = monthly_sales.iloc[0]

lowest_month = monthly_sales.index[-1]
lowest_month_sales = monthly_sales.iloc[-1]

month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

# 7. Order status
status_counts = orders["status"].value_counts()

# 8. ML result
ridge_r2 = -0.0385


findings = f"""
Finding 1:
Finding: {top_category} has the highest sales.
Evidence: {top_category} sales = ₹{top_category_sales:,.0f}.
Analysis to use: Analyze {top_category} sales by city and state.

Finding 2:
Finding: {top_product} is the highest-selling product.
Evidence: {top_product} sales = ₹{top_product_sales:,.0f}.
Analysis to use: Analyze {top_product} sales by city, state, and month.

Finding 3:
Finding: {top_brand} is the highest-selling brand.
Evidence: {top_brand} sales = ₹{top_brand_sales:,.0f}.
Analysis to use: Analyze {top_brand} sales by product and city.

Finding 4:
Finding: {top_city} has the highest sales among cities.
Evidence: {top_city} sales = ₹{top_city_sales:,.0f}.
Analysis to use: Analyze {top_city} sales by product, brand, and order status.

Finding 5:
Finding: {month_names[highest_month]} has the highest monthly sales.
Evidence: {month_names[highest_month]} sales = ₹{highest_month_sales:,.0f}.
Analysis to use: Analyze {month_names[highest_month]} sales by category and product.

Finding 6:
Finding: {month_names[lowest_month]} has the lowest monthly sales.
Evidence: {month_names[lowest_month]} sales = ₹{lowest_month_sales:,.0f}.
Analysis to use: Analyze {month_names[lowest_month]} sales by category and product.

Finding 7:
Finding: Order status counts are {status_counts.to_dict()}.
Evidence: These are the order counts by status.
Analysis to use: Analyze pending and cancelled orders by product, city, and month.

Finding 8:
Finding: Ridge Regression produced R² = {ridge_r2}.
Evidence: R² = {ridge_r2}.
Analysis to use: Review the available ML features and compare the model with a simple baseline.
"""

    
prompt = f"""
You are an AI business analyst.

VERIFIED FINDINGS:
{findings}

For each of the 8 findings, provide:
1. The verified finding.
2. A recommended analysis/action.
3. A practical way to improve or investigate the situation.

STRICT RULES:
- Give exactly 8 findings.
- Do not change any verified fact or number.
- Do not invent causes or business conditions.
- Do not claim something is causing a result unless the data proves it.
- "How to improve" must be based only on the analysis requested.
- Keep each section short.
- Do not mention Python, Pandas, SQL, or other tools.

Use EXACTLY this format:

Finding 1:
Finding: [verified finding]
Recommendation: [recommended analysis/action]
How to improve: [practical next step based on the analysis]

Finding 2:
Finding: [verified finding]
Recommendation: [recommended analysis/action]
How to improve: [practical next step based on the analysis]

Continue the same format through Finding 8.
"""


response = ollama.chat(
    model="deepseek-r1:7b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response["message"]["content"])



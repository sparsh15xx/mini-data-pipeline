import pandas as pd

# Fetch all data
response = supabase.table("customer_orders").select("*").execute()
data = response.data
df = pd.DataFrame(data)

# Ensure correct types
df['quantity'] = df['quantity'].astype(int)
df['price_per_unit'] = df['price_per_unit'].astype(float)
df['order_date'] = pd.to_datetime(df['order_date'])
df['total_spend'] = df['quantity'] * df['price_per_unit']

# Top 5 customers by total spend
top_customers = df.groupby('customer_name')['total_spend'].sum().sort_values(ascending=False).head(5)

# Most popular product by quantity sold
top_product = df.groupby('product_name')['quantity'].sum().sort_values(ascending=False).head(1)

# Average order value
avg_order_value = df['total_spend'].mean()

# Number of orders each week for the past 8 weeks
df['week'] = df['order_date'].dt.to_period('W').apply(lambda r: r.start_time)
recent_weeks = df[df['order_date'] >= (pd.Timestamp.now() - pd.Timedelta(weeks=8))]
orders_per_week = recent_weeks.groupby('week').size()

print("Top 5 Customers by Total Spend:\n", top_customers)
print("\nMost Popular Product:\n", top_product)
print("\nAverage Order Value: {:.2f}".format(avg_order_value))
print("\nOrders per Week (last 8 weeks):\n", orders_per_week)

import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key="AIzaSyBngNrnRXlKPflE0nmUdjG6C95CA-mYwhs")

# Use the Gemini Pro model (free tier supports this)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Your analysis results as a prompt
analysis_text = """
Top 5 Customers by Total Spend:
Ashley Weber: 1984.90
Andrea Ramos: 1911.60
Ronald Smith V: 1811.60
Andrew Rivera: 1776.42
Justin Hammond: 1772.80

Most Popular Product:
Gizmo (542 units sold)

Average Order Value: 599.72

Orders per Week (last 8 weeks):
2025-03-10: 12
2025-03-17: 47
2025-03-24: 39
2025-03-31: 47
2025-04-07: 35
2025-04-14: 38
2025-04-21: 39
2025-04-28: 38
2025-05-05: 24

Summarize these findings in bullet points for an executive and suggest a marketing insight based on the data.
"""

# Generate the summary and insight
response = model.generate_content(analysis_text)

print("Executive Summary & Marketing Insight:\n")
print(response.text)
from supabase import create_client, Client
from faker import Faker
import random
from datetime import datetime, timedelta

SUPABASE_URL = "https://ozfqzskqwzoyiiwmhbhm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96ZnF6c2txd3pveWlpd21oYmhtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY3ODg3NzYsImV4cCI6MjA2MjM2NDc3Nn0.1VcsxCQl5CtB-GQOpRGBQrTw9n5-hFhVVB8u35GlcGg"
supabase: Client = create_client(
    "https://ozfqzskqwzoyiiwmhbhm.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96ZnF6c2txd3pveWlpd21oYmhtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY3ODg3NzYsImV4cCI6MjA2MjM2NDc3Nn0.1VcsxCQl5CtB-GQOpRGBQrTw9n5-hFhVVB8u35GlcGg"
)
fake = Faker()
products = ['Widget', 'Gadget', 'Doodad', 'Thingamajig', 'Doohickey', 'Gizmo']
rows = []
for _ in range(500):
    customer_name = fake.name()
    product_name = random.choice(products)
    quantity = random.randint(1, 10)
    price_per_unit = round(random.uniform(10, 200), 2)
    days_ago = random.randint(0, 89)
    order_date = datetime.now() - timedelta(days=days_ago)
    rows.append({
        "customer_name": customer_name,
        "product_name": product_name,
        "quantity": quantity,
        "price_per_unit": price_per_unit,
        "order_date": order_date.isoformat()
    })
# Batch insert (Supabase recommends batches of 100 or less)
for i in range(0, 500, 100):
    batch = rows[i:i+100]
    supabase.table("customer_orders").insert(batch).execute()
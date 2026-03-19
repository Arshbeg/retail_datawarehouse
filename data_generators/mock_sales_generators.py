import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

# Set Faker to French locale for realistic Carrefour data
fake = Faker('fr_FR')

# --- CONFIGURATION ---
NUM_STORES = 200
NUM_PRODUCTS = 100000
NUM_CUSTOMERS = 50000
NUM_RECEIPTS = 2000000 
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 2, 28)

def generate_carrefour_data():
    print("🛒 Starting Carrefour Mock Data Generation...")

    # 1. Generate Stores (dim_stores)
    store_formats = ['Hyper', 'Market', 'City', 'Express']
    stores = []
    for i in range(1, NUM_STORES + 1):
        stores.append({
            'store_id': i,
            'store_name': f"Carrefour {fake.city()}",
            'format': random.choice(store_formats),
            'region': fake.region()
        })
    df_stores = pd.DataFrame(stores)
    
    # 2. Generate Products (dim_products)
    categories = {
        'Epicerie Salée': ['Pâtes', 'Riz', 'Conserves'],
        'Produits Frais': ['Lait', 'Beurre', 'Fromage', 'Viande', 'Fruits', 'Légumes'],
        'Liquides': ['Eau', 'Jus', 'Soda', 'Vin'],
        'Hygiène & Beauté': ['Shampooing', 'Savon', 'Dentifrice']
    }
    
    products = []
    for i in range(1, NUM_PRODUCTS + 1):
        cat = random.choice(list(categories.keys()))
        sub_cat = random.choice(categories[cat])
        base_price = round(random.uniform(0.99, 25.99), 2)
        
        products.append({
            'product_id': i,
            'product_name': f"{sub_cat} {fake.word().capitalize()}",
            'category': cat,
            'sub_category': sub_cat,
            'brand': 'Carrefour' if random.random() > 0.7 else fake.company(),
            'unit_price': base_price,
            'cost_price': round(base_price * random.uniform(0.4, 0.8), 2) # Profit margin logic
        })
    df_products = pd.DataFrame(products)

    # 3. Generate Customers (dim_customers)
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        customers.append({
            'customer_id': i,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'loyalty_card_number': fake.ean13(),
            'postal_code': fake.postcode()
        })
    df_customers = pd.DataFrame(customers)

    # 4. Generate Sales / Receipts (fact_sales)
    sales = []
    transaction_id = 1
    
    print(f"Generating {NUM_RECEIPTS} receipts...")
    for receipt_id in range(1, NUM_RECEIPTS + 1):
        # Receipt-level details
        store_id = random.choice(df_stores['store_id'])
        # 30% of customers don't use a loyalty card (represented as NULL or 0)
        customer_id = random.choice(df_customers['customer_id']) if random.random() > 0.3 else None
        
        # Random timestamp within our date range
        random_days = random.randint(0, (END_DATE - START_DATE).days)
        random_seconds = random.randint(0, 86400)
        txn_datetime = START_DATE + timedelta(days=random_days, seconds=random_seconds)
        
        # A basket contains 1 to 15 items
        basket_size = random.randint(1, 15)
        basket_products = random.sample(products, basket_size)
        
        for prod in basket_products:
            qty = random.randint(1, 4)
            sales.append({
                'transaction_id': transaction_id,
                'receipt_id': receipt_id,
                'store_id': store_id,
                'customer_id': customer_id,
                'product_id': prod['product_id'],
                'transaction_date': txn_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'quantity': qty,
                'gross_amount': round(qty * prod['unit_price'], 2)
            })
            transaction_id += 1

    df_sales = pd.DataFrame(sales)

    # --- SAVE TO CSV ---
    # Create a raw_data folder if it doesn't exist
    os.makedirs('raw_data', exist_ok=True)
    
    df_stores.to_csv('raw_data/stores.csv', index=False)
    df_products.to_csv('raw_data/products.csv', index=False)
    df_customers.to_csv('raw_data/customers.csv', index=False)
    df_sales.to_csv('raw_data/sales.csv', index=False)

    print("✅ Success! Generated raw data files in the 'raw_data' folder.")
    print(f"Total line items generated: {len(df_sales)}")

if __name__ == "__main__":
    generate_carrefour_data()
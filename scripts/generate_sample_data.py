"""
E-Commerce Sample Data Generator
Generates realistic sample data for the data warehouse project
"""

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Initialize Faker
fake = Faker()
Faker.seed(42)  # For reproducibility
random.seed(42)

# Create data directory if it doesn't exist
os.makedirs('data/raw', exist_ok=True)

print("Starting data generation...")

# ============================================
# 1. GENERATE LOCATIONS
# ============================================
print("Generating locations...")

locations = []
location_types = ['Store', 'Warehouse', 'Distribution Center']
regions = {
    'Northeast': ['New York', 'Boston', 'Philadelphia', 'Newark'],
    'Southeast': ['Atlanta', 'Miami', 'Charlotte', 'Tampa'],
    'Midwest': ['Chicago', 'Detroit', 'Minneapolis', 'Cleveland'],
    'Southwest': ['Houston', 'Dallas', 'Phoenix', 'San Antonio'],
    'West': ['Los Angeles', 'San Francisco', 'Seattle', 'Portland']
}

location_id = 1
for region, cities in regions.items():
    for city in cities:
        for loc_type in location_types[:2]:  # Store and Warehouse only
            locations.append({
                'location_key': f'LOC-{location_id:04d}',
                'location_name': f'{city} {loc_type}',
                'location_type': loc_type,
                'address_line1': fake.street_address(),
                'city': city,
                'state': fake.state_abbr(),
                'postal_code': fake.zipcode(),
                'country': 'USA',
                'region': region,
                'latitude': fake.latitude(),
                'longitude': fake.longitude(),
                'is_active': True,
                'open_date': fake.date_between(start_date='-5y', end_date='-1y')
            })
            location_id += 1

df_locations = pd.DataFrame(locations)
df_locations.to_csv('data/raw/locations.csv', index=False)
print(f"✓ Generated {len(locations)} locations")

# ============================================
# 2. GENERATE CUSTOMERS
# ============================================
print("Generating customers...")

customers = []
customer_segments = ['VIP', 'Regular', 'New']
loyalty_tiers = ['Gold', 'Silver', 'Bronze', None]

for i in range(1, 1001):
    join_date = fake.date_between(start_date='-3y', end_date='today')
    
    customers.append({
        'customer_key': f'CUST-{i:06d}',
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80),
        'gender': random.choice(['Male', 'Female', 'Other']),
        'address_line1': fake.street_address(),
        'address_line2': fake.secondary_address() if random.random() < 0.3 else None,
        'city': fake.city(),
        'state': fake.state_abbr(),
        'postal_code': fake.zipcode(),
        'country': 'USA',
        'customer_segment': random.choice(customer_segments),
        'loyalty_tier': random.choice(loyalty_tiers),
        'join_date': join_date
    })

df_customers = pd.DataFrame(customers)
df_customers.to_csv('data/raw/customers.csv', index=False)
print(f"✓ Generated {len(customers)} customers")

# ============================================
# 3. GENERATE PRODUCTS
# ============================================
print("Generating products...")

# Product categories and subcategories
product_categories = {
    'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Accessories', 'Smart Home'],
    'Clothing': ['Men\'s Wear', 'Women\'s Wear', 'Kids Wear', 'Shoes', 'Accessories'],
    'Home & Garden': ['Furniture', 'Kitchen', 'Bedding', 'Decor', 'Garden Tools'],
    'Sports & Outdoors': ['Fitness', 'Camping', 'Cycling', 'Team Sports', 'Water Sports'],
    'Books & Media': ['Fiction', 'Non-Fiction', 'Educational', 'Movies', 'Music']
}

brands = ['TechPro', 'StyleMax', 'HomeComfort', 'FitGear', 'SmartLife', 
          'EcoChoice', 'LuxeLine', 'ValueBrand', 'Premium Plus', 'BasicGoods']

sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL', None]
colors = ['Black', 'White', 'Blue', 'Red', 'Green', 'Gray', 'Navy', None]

products = []
product_id = 1

for category, subcategories in product_categories.items():
    for subcategory in subcategories:
        # Generate 20 products per subcategory
        for i in range(20):
            cost_price = round(random.uniform(10, 500), 2)
            markup = random.uniform(1.3, 2.5)  # 30-150% markup
            unit_price = round(cost_price * markup, 2)
            
            products.append({
                'product_key': f'PROD-{product_id:06d}',
                'product_name': f'{fake.word().title()} {subcategory} {fake.word().title()}',
                'product_description': fake.sentence(nb_words=12),
                'category': category,
                'subcategory': subcategory,
                'brand': random.choice(brands),
                'supplier': fake.company(),
                'unit_price': unit_price,
                'cost_price': cost_price,
                'size': random.choice(sizes),
                'color': random.choice(colors),
                'weight': round(random.uniform(0.1, 20), 2),
                'weight_unit': 'lbs',
                'is_active': random.random() > 0.05,  # 95% active
                'discontinued_date': None
            })
            product_id += 1

df_products = pd.DataFrame(products)
df_products.to_csv('data/raw/products.csv', index=False)
print(f"✓ Generated {len(products)} products")

# ============================================
# 4. GENERATE PAYMENT METHODS
# ============================================
print("Generating payment methods...")

payment_methods = [
    {'payment_type': 'Credit Card', 'payment_provider': 'Visa'},
    {'payment_type': 'Credit Card', 'payment_provider': 'Mastercard'},
    {'payment_type': 'Credit Card', 'payment_provider': 'American Express'},
    {'payment_type': 'Debit Card', 'payment_provider': 'Visa'},
    {'payment_type': 'Debit Card', 'payment_provider': 'Mastercard'},
    {'payment_type': 'Digital Wallet', 'payment_provider': 'PayPal'},
    {'payment_type': 'Digital Wallet', 'payment_provider': 'Apple Pay'},
    {'payment_type': 'Digital Wallet', 'payment_provider': 'Google Pay'},
]

df_payment_methods = pd.DataFrame(payment_methods)
df_payment_methods.to_csv('data/raw/payment_methods.csv', index=False)
print(f"✓ Generated {len(payment_methods)} payment methods")

# ============================================
# 5. GENERATE SHIPPING METHODS
# ============================================
print("Generating shipping methods...")

shipping_methods = [
    {'shipping_type': 'Standard', 'carrier': 'USPS', 'estimated_days': 7},
    {'shipping_type': 'Standard', 'carrier': 'UPS', 'estimated_days': 5},
    {'shipping_type': 'Express', 'carrier': 'FedEx', 'estimated_days': 2},
    {'shipping_type': 'Express', 'carrier': 'UPS', 'estimated_days': 2},
    {'shipping_type': 'Overnight', 'carrier': 'FedEx', 'estimated_days': 1},
    {'shipping_type': 'Overnight', 'carrier': 'UPS', 'estimated_days': 1},
]

df_shipping_methods = pd.DataFrame(shipping_methods)
df_shipping_methods.to_csv('data/raw/shipping_methods.csv', index=False)
print(f"✓ Generated {len(shipping_methods)} shipping methods")

# ============================================
# 6. GENERATE ORDERS
# ============================================
print("Generating orders... (this may take a moment)")

orders = []
order_statuses = ['Delivered', 'Shipped', 'Processing', 'Cancelled']
status_weights = [0.70, 0.15, 0.10, 0.05]  # 70% delivered, etc.

# Generate orders over the past 2 years
start_date = datetime.now() - timedelta(days=730)
end_date = datetime.now()

order_number = 1000
for i in range(15000):  # Generate 15,000 order lines
    # Determine if this is a new order or continuation
    if i == 0 or random.random() < 0.7:  # 70% chance of new order
        order_number += 1
        line_number = 1
        
        # Order-level attributes
        customer = random.choice(customers)
        order_date = fake.date_time_between(start_date=start_date, end_date=end_date)
        order_status = random.choices(order_statuses, weights=status_weights)[0]
        
        # Ship date (if shipped or delivered)
        if order_status in ['Shipped', 'Delivered']:
            ship_date = order_date + timedelta(days=random.randint(1, 3))
        else:
            ship_date = None
            
        location = random.choice(locations)
        payment_method = random.choice(payment_methods)
        shipping_method = random.choice(shipping_methods)
        
        order_total = 0
    else:
        line_number += 1
    
    # Line-level attributes
    product = random.choice(products)
    quantity = random.randint(1, 5)
    unit_price = product['unit_price']
    unit_cost = product['cost_price']
    
    # Apply discounts randomly
    discount_amount = 0
    if random.random() < 0.2:  # 20% of orders get a discount
        discount_amount = round(unit_price * quantity * random.uniform(0.05, 0.25), 2)
    
    line_total = round((unit_price * quantity) - discount_amount, 2)
    line_profit = round(line_total - (unit_cost * quantity), 2)
    tax_amount = round(line_total * 0.08, 2)  # 8% tax
    
    # Shipping cost (only on first line of order)
    if line_number == 1:
        shipping_cost = round(random.uniform(5, 15), 2)
    else:
        shipping_cost = 0
    
    order_total += line_total + tax_amount + shipping_cost
    
    orders.append({
        'order_number': f'ORD-{order_number:08d}',
        'order_line_number': line_number,
        'customer_key': customer['customer_key'],
        'product_key': product['product_key'],
        'order_date': order_date.strftime('%Y-%m-%d'),
        'ship_date': ship_date.strftime('%Y-%m-%d') if ship_date else None,
        'location_key': location['location_key'],
        'payment_type': payment_method['payment_type'],
        'payment_provider': payment_method['payment_provider'],
        'shipping_type': shipping_method['shipping_type'],
        'carrier': shipping_method['carrier'],
        'quantity': quantity,
        'unit_price': unit_price,
        'unit_cost': unit_cost,
        'discount_amount': discount_amount,
        'tax_amount': tax_amount,
        'shipping_cost': shipping_cost,
        'line_total': line_total,
        'line_profit': line_profit,
        'order_total': round(order_total, 2),
        'order_status': order_status
    })

df_orders = pd.DataFrame(orders)
df_orders.to_csv('data/raw/orders.csv', index=False)
print(f"✓ Generated {len(orders)} order lines across {order_number - 999} orders")

# ============================================
# SUMMARY
# ============================================
print("\n" + "="*50)
print("DATA GENERATION COMPLETE!")
print("="*50)
print(f"✓ Locations: {len(locations)}")
print(f"✓ Customers: {len(customers)}")
print(f"✓ Products: {len(products)}")
print(f"✓ Payment Methods: {len(payment_methods)}")
print(f"✓ Shipping Methods: {len(shipping_methods)}")
print(f"✓ Order Lines: {len(orders)}")
print(f"✓ Unique Orders: {order_number - 999}")
print("\nAll CSV files saved to: data/raw/")

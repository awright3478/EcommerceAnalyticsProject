SET search_path TO ecommerce_dw;

CREATE TABLE dim_customer(
    customer_id SERIAL PRIMARY KEY,
    customer_key VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    full_name VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(20),
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    customer_segment VARCHAR(50),
    loyalty_tier VARCHAR(50),
    join_date DATE NOT NULL,
    effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
    expiration_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_product (
    product_id SERIAL PRIMARY KEY,
    product_key VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_description TEXT,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    supplier VARCHAR(100),
    unit_price DECIMAL(10,2),
    cost_price DECIMAL(10,2),

    size VARCHAR(50),
    color VARCHAR(50),
    weight VARCHAR(50),
    weight_unit VARCHAR(50),

    is_active BOOLEAN DEFAULT TRUE,
    discontinued_at DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,  
    full_date DATE UNIQUE NOT NULL,
    day_of_week INTEGER,       
    day_name VARCHAR(20),    
    day_of_month INTEGER,
    day_of_year INTEGER,
    week_of_year INTEGER,
    month_number INTEGER,
    month_name VARCHAR(20),
    month_abbr VARCHAR(3),
    quarter INTEGER,
    quarter_name VARCHAR(10),     
    year INTEGER,
    
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    holiday_name VARCHAR(100),
  
    fiscal_year INTEGER,
    fiscal_quarter INTEGER,
    fiscal_month INTEGER,
 
    year_month VARCHAR(7),         
    year_quarter VARCHAR(7)       
);

CREATE TABLE dim_location (
    location_id SERIAL PRIMARY KEY,
    location_key VARCHAR(50) UNIQUE NOT NULL,
    location_name VARCHAR(255),
    location_type VARCHAR(50), -- 'Store', 'Warehouse', 'Distribution Center'
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    region VARCHAR(100),
    latitude DECIMAL(10,8),
    longitude DECIMAL(10,8),
    
    is_active BOOLEAN DEFAULT TRUE,
    open_date DATE,
    cose_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_payment_method (
    payment_method_id SERIAL PRIMARY KEY,
    payment_type VARCHAR(50) NOT NULL,
    payment_provider VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE dim_shipping_method (
    shipping_method_id SERIAL PRIMARY KEY,
    shipping_type VARCHAR(50) NOT NULL,
    carrier VARCHAR(100),
    estimated_days INTEGER,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE fact_sales(
    sales_id BIGSERIAL PRIMARY KEY,

    customer_id INTEGER NOT NULL REFERENCES dim_customer(customer_id),
    product_id INTEGER NOT NULL REFERENCES dim_product(product_id),
    order_date_id INTEGER REFERENCES dim_date(date_id),
    ship_date_id INTEGER  REFERENCES dim_date(date_id),
    location_id INTEGER REFERENCES dim_location(location_id),
    payment_method_id INTEGER REFERENCES dim_payment_method(payment_method_id),
    shipping_method_id INTEGER REFERENCES dim_shipping_method(shipping_method_id),

    order_number VARCHAR(50) NOT NULL,
    order_line_number INTEGER NOT NULL,

    quantity INTEGER NOT NULL,
    unit_price DEC(10,2) NOT NULL,
    unit_cost DEC(10,2),
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    shipping_cost DECIMAL(10,2) DEFAULT 0,

    line_total DECIMAL(10,2) NOT NULL,
    line_profit DECIMAL(10,2),

    order_total DECIMAL(10,2),
    order_status VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(order_number, order_line_number)
);

CREATE TABLE fact_inventory_daily(
    inventory_id BIGSERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES dim_product(product_id),
    location_id INTEGER NOT NULL REFERENCES dim_location(location_id),
    snapshot_date_id INTEGER NOT NULL REFERENCES dim_date(date_id),

    quantity_on_hand INTEGER NOT NULL,
    quantity_allocated INTEGER DEFAULT 0,
    quantity_available INTEGER NOT NULL,
    reorder_point INTEGER,
    reorder_quantity INTEGER,
    unit_cost DECIMAL(10,2),
    inventory_value DECIMAL(10,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, location_id, snapshot_date_id)
);

CREATE TABLE fact_customer_activity(
    activity_id BIGSERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES dim_customer(customer_id),

    first_order_date_id INTEGER REFERENCES dim_date(date_id),
    last_order_date_id INTEGER REFERENCES dim_date(date_id),
    snapshot_date_id INTEGER NOT NULL REFERENCES dim_date(date_id),

    total_orders INTEGER DEFAULT 0,
    total_items_purchase INTEGER DEFAULT 0,
    total_amount_spent DECIMAL(12,2) DEFAULT 0,
    average_order_value DECIMAL(10,2) DEFAULT 0,
    days_since_last_order INTEGER,

    customer_lifetime_value DECIMAL(12,2) DEFAULT 0,
    recency_score INTEGER,
    frequency_score INTEGER,
    monetary_score INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(customer_id, snapshot_date_id)
);


COMMENT ON TABLE dim_customer IS 'Customer dimension with Type 2 SCD for tracking address changes';
COMMENT ON TABLE dim_product IS 'Product dimension with current product information';
COMMENT ON TABLE dim_date IS 'Date dimension covering all dates needed for analysis';
COMMENT ON TABLE dim_location IS 'Location dimension for stores, warehouses, and distribution centers';
COMMENT ON TABLE fact_sales IS 'Transaction fact table at order line item grain';
COMMENT ON TABLE fact_inventory_daily IS 'Daily snapshot of inventory levels by product and location';
COMMENT ON TABLE fact_customer_activity IS 'Accumulating snapshot of customer purchase behavior';
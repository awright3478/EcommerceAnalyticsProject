SET search_path TO ecommerce_dw;

CREATE INDEX idx_customer_email ON dim_customer(email);
CREATE INDEX idx_customer_join_date ON dim_customer(join_date);
CREATE INDEX idx_customer_city ON dim_customer(city);
CREATE INDEX idx_customer_state ON dim_customer(state);
CREATE INDEX idx_customer_segment ON dim_customer(customer_segment);
CREATE INDEX idx_customer_is_current ON dim_customer(is_current);
CREATE INDEX idx_customer_effective_date ON dim_customer(effective_date, expiration_date);

CREATE INDEX idx_product_category ON dim_product(category);
CREATE INDEX idx_product_subcategory ON dim_product(subcategory);
CREATE INDEX idx_product_brand ON dim_product(brand);
CREATE INDEX idx_product_name ON dim_product(product_name);
CREATE INDEX idx_product_is_active ON dim_product(is_active);

CREATE INDEX idx_date_full_date ON dim_date(full_date);
CREATE INDEX idx_date_year_month ON dim_date(year, month_number);
CREATE INDEX idx_date_quarter ON dim_date(year, quarter);
CREATE INDEX idx_date_is_weekend ON dim_date(is_weekend);
CREATE INDEX idx_date_is_holiday ON dim_date(is_holiday);

CREATE INDEX idx_location_city ON dim_location(city);
CREATE INDEX idx_location_state ON dim_location(state);
CREATE INDEX idx_location_region ON dim_location(region);
CREATE INDEX idx_location_type ON dim_location(location_type);
CREATE INDEX idx_location_is_actiive ON dim_location(is_active);


CREATE INDEX idx_sales_customer_id ON fact_sales(customer_id);
CREATE INDEX idx_sales_produce_id ON fact_sales(product_id);
CREATE INDEX idx_sales_order_date_id ON fact_sales(order_date_id);
CREATE INDEX idx_sales_ship_date_id ON fact_sales(ship_date_id);
CREATE INDEX idx_sales_location_id ON fact_sales(location_id);
CREATE INDEX idx_sales_payment_method_id ON fact_sales(payment_method_id);
CREATE INDEX idx_sales_shipping_method_id ON fact_sales(shipping_method_id);

CREATE INDEX idx_sales_order_number ON fact_sales(order_number);
CREATE INDEX idx_sales_order_status ON fact_sales(order_status);
CREATE INDEX idx_sales_created_at ON fact_sales(created_at);

CREATE INDEX idx_sales_customer_date ON fact_sales(customer_id, order_date_id);
CREATE INDEX idx_sales_product_date ON fact_sales(product_id, order_date_id);
CREATE INDEX idx_sales_date_status ON fact_sales(order_date_id, order_status);

CREATE INDEX idx_inventory_product_id ON fact_inventory_daily(product_id);
CREATE INDEX idx_inventory_location_id ON fact_inventory_daily(location_id);
CREATE INDEX idx_inventory_snaphsot_date_id ON fact_inventory_daily(snapshot_date_id);
CREATE INDEX idx_inventory_product_location ON fact_inventory_daily(product_id, location_id);
CREATE INDEX idx_inventory_date_location ON fact_inventory_daily(snapshot_date_id, location_id);

CREATE INDEX idx_activity_customer_id ON fact_customer_activity(customer_id);
CREATE INDEX idx_activity_snaphshot_date_id ON fact_customer_activity(snapshot_date_id);
CREATE INDEX idx_activity_last_order_date ON fact_customer_activity(last_order_date_id);
CREATE INDEX idx_activity_rfm_scores ON  fact_customer_activity(recency_score, frequency_score);

ANALYZE dim_customer;
ANALYZE dim_product;
ANALYZE dim_date;
ANALYZE dim_location;
ANALYZE dim_payment_method;
ANALYZE dim_shipping_method;
ANALYZE fact_sales;
ANALYZE fact_inventory_daily;
ANALYZE fact_customer_activity;





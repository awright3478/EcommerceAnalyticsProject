# EcommerceAnalyticsProject
A data engineering project demonstrating database design, data generation, and SQL analytics for an e-commerce platform using Python and PostgreSQL.

Project Overview
Thsi Project showcases core data engineering skills through a complete e-commerce data warehouse implementation featuring dimensional modeling, realistic data generation, and analytical SQL queries.
Key Achievements:
    -Designed and implemented a star schema data warehouse optimized for analytics
    -Generated 15,000+ realistic e-commerce transactions using Python
    -Created complex SQL queries demonstrating advanced analytical capabilities
    -Estbalished professional project structure structure with comprehensive documentation
Completed Features
    -Database Design
    -Data Generation
    -SQL Analytics
Technology Stack
    -Python 3.12 - For data generation and scripting
    -SQL - For database design and analytics
    -PostgreSQL 14+ - Relational data warehouse
    -Git - Version control
    Python Libraries
        -Faker - Realistic data generation
        -Pandas - Data manipulation (ready for ETL expansion)

Project Structure
EcommerceAnalyticsProject/
├── data/
│   └─ raw/                    # Generated CSV files
│       ├─ customers.csv       # 1,000 customers
│       ├─ products.csv        # 500 products
│       ├─ orders.csv          # 15,000+ order lines
│       ├─ locations.csv       # 40 locations
│       ├─ payment_methods.csv # 8 payment types
│       └─ shipping_methods.csv # 6 shipping options
│
├── scripts/
│   └─ generate_sample_data.py # Data generation script
│
├── sql/
│   ├─ ddl/                    # Data Definition Language
│   │   ├─ create_schema.sql   # Schema creation
│   │   ├──create_tables.sql   # Table definitions
│   │   └─ create_indexes.sql  # Index creation
│   ├─ dml/                    # Data Manipulation Language
│   │   └─ populate_date_dimension.sql
│   └── queries/                # Analytics queries
│       ├─ customer_analytics.sql
│       ├─ product_performance.sql
│       └─ sales_trends.sql
│
├─ .gitignore
├─ README.md
└─ requirements.txt

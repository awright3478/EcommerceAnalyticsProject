"""
Main ETL Pipeline
Orchestrates the complete ETL process
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from src.extractors.csv_extractor import CSVExtractor
from src.transformers.customer_transformer import CustomerTransformer
from src.transformers.product_transformer import ProductTransformer
from src.transformers.sales_transformer import SalesTransformer
from src.loaders.warehouse_loader import WarehouseLoader
from src.utils.logger import setup_logger
from datetime import datetime

class EcommercePipeline:
    """
    Main ETL Pipeline for E-Commerce Data Warehouse
    """

    def __init__(self):
        self.logger = setup_logger('main_pipeline', 'etl_pipeline.log')
        self.loader = None
        self.start_time = None
        self.end_time = None
    
    def run(self):
        """
        Execute the complete ETL pipeline
        """
        self.start_time = datetime.now()
        self.logger.info("="*60)
        self.logger.info("Starting E-Commerce ETL Pipeline")
        self.logger.info("="*60)
        try:
            self.loader = WarehouseLoader()
            self.loader.connect

            self.logger.info("\n--- Step 1: Loading Reference Data ---")
            self.load_reference_data()

            self.logger.info("\n--- Step 2: Loading Dimension Tables ---")
            self.load_dimensions()

            self.logger.info("\n--- Step 3: Loading Fact Tables ---")
            self.load_facts()

            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds()

            self.logger.info("=" * 60)
            self.logger.info(f"ETL Pipeline completed successfully in {duration:.2f} seconds")
            self.logger.info("="*60)

        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise
        finally:
            if self.loader:
                self.loader.disconnect()

    def load_reference_data(self):
        """
        Load payment and shipping methods
        """
        extractor = CSVExtractor('payment_methods.csv')
        df_payment = extractor.extract()
        self.loader.load_payment_methods(df_payment)

        extractor = CSVExtractor('shipping_methods.csv')
        df_shipping = extractor.extract()
        self.loader.load_shipping_methods(df_shipping)

        self.logger.info(f"Reference data succesfully loaded")

    def load_dimensions(self):
        """
        Load all dimension tables
        """
        self.logger.info("Loading customers...")
        extractor = CSVExtractor('customers.csv')
        df_customers = extractor.extract()

        transformer = CustomerTransformer()
        df_customers = transformer.transform(df_customers)

        self.loader.load_customers(df_customers)

        self.logger.info("Loading products...")
        extractor = CSVExtractor('products.csv')
        df_products = extractor.extract()

        transformer = ProductTransformer()
        df_products = transformer.transform(df_products)

        self.loader.load_products(df_products)

        self.logger.info("Loading locations...")
        extractor = CSVExtractor('loactions.csv')
        df_locations = extractor.extract()

        self.loader.load_locations(df_locations)

        self.logger.info("All dimensions loaded successfully")

    def load_facts(self):
        """
        Load all fact tables
        """
        self.logger.info("Loading sales...")
        extractor = CSVExtractor('sales.csv')
        df_sales = extractor.extract()

        transformer = SalesTransformer()
        df_sales = transformer.transform(df_sales)

        self.loader.load_sales(df_sales)
        self.logger.info("All facts loaded succesfully")

    def main():
        """Main entry point of program"""
        pipeline = EcommercePipeline()
        pipeline.run()
    if __name__ == '__main__':
        main()


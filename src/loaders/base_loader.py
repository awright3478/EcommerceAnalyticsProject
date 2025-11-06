"""
Base Loader Class
Abstract base class for all data loaders
"""
from abc import ABC, abstractmethod
import psycogg2
from psycopg2.extras import execute_branch
from config.database import DatabaseConfig
from src.utils.logger import setup_logger

class BaseLoader(ABC):
    """
    Base Loader Class
    Abstract base class for all data loaders
    """
    def __init__(self, target_name):
        """
        Initialize loader
        Args:
            target_name: name of the target
        """
        self.target_name = target_name
        self.logger = setup_logger(f'loader.{target_name}')
        self.db_config = DatabaseConfig()
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish connection database"""
        try:
            self.logger.info("Connecting to database...")
            self.conn = psycopg2.connect(**self.db_config.get_connection_string())
            self.cursor = self.conn.cursor()

            self.cursor.execute(f"SET search_path TO {self.db_config.schema}")
            self.conn.commit()

            self.logger.info("Database connection established")
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {str(e)}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.logger.info(f"Database connection closed")

    @abstractmethod
    def load(self, df):
        """
        Load data into target table
        Must be implemented by subclass

        Args:   
            df: DataFrame to load
        Returns:
            int: Number of rows loaded
        """
        pass
    
    def turnucate_table(self, table_name):
        """
        Trunucate target table

        Args:
            table_name: name of the table to trunucate
        """
        try:
            self.logger.warning(f"Trunucating table: {table_name}")
            self.cursor.execute(f"TRUNUCATE TABLE {table_name} CASCADE")
            self.conn.commit()
            self.logger.info(f"Table {table_name} trunucated succesfully")
        except Exception as e:
            self.logger.error(f"Error trunucating table {table_name}: {str(e)}")
            self.conn.rollback()
            raise
    
    def execute_batch_insert(self, sql, data, batch_size=1000):
        """
        Execute batch insert

        Args: 
            sql: INSERT SQL statement
            data: List of tuples to insert
            batch_size: Number of rows per batch

        Returns:
            int: Number of rows inserted
        """
        try:
            execute_batch(self.cursor, sql, data, page_size=batch_size)
            self.conn.commit()
            return len(data)
        except Exception as e:
            self.logger.error(f"Error executing batch insert: {str(e)}")
            self.conn.rollback()
            raise
    



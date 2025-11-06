"""
Database Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

def __init__(self):
    self.host = os.getenv('DB_HOST', 'localhost')
    self.port = os.getenv('DB_PORT', '5432')
    self.database = os.getenv('DB_NAME', 'ecommerce_dw')
    self.user = os.getenv('DB_USER', os.getenv('USER'))
    self.password = os.getenv('DB_PASSWORD', '')
    self.schema = 'ecommerce_dw'
    
def get_connection_string(self):
    """Returns PostgreSQL connection string"""
    if self.password:
        return f"posgresql://{self.user}{self.password}@{self.host}:{self.port}/{self.database}"
    else:
        return f"postgreswl://{self.user}@{self.host}:{self.port}/{self.database}"

def get_connection_params(self):
    """Returns connection paramaters as dictionary"""
    params = {
        'host' :self.host,
        'port': self.port,
        'database':self.database,
        'user': self.user
    }
    if self.password:
        params['password'] = self.password
    return params
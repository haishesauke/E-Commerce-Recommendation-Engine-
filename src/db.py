# src/db.py
from sqlalchemy import create_engine
import pandas as pd
import os

DB_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@127.0.0.1:3306/ecom')

def get_engine():
    return create_engine(DB_URI)

def load_transactions(limit=None):
    engine = get_engine()
    q = "SELECT user_id, item_id, action, price, created_at FROM transactions"
    if limit:
        q += f" LIMIT {limit}"
    return pd.read_sql(q, engine)

def load_items():
    engine = get_engine()
    return pd.read_sql("SELECT id, sku, title, category FROM items", engine)

# src/utils.py
import pandas as pd
import random
from datetime import datetime, timedelta
import os

OUT_TX = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_transactions.csv')
OUT_ITEMS = os.path.join(os.path.dirname(__file__), '..', 'data', 'items.csv')

ACTIONS = ['view','click','cart','purchase']

def generate(n_users=200, n_items=100, n_events=5000, out_tx=OUT_TX, out_items=OUT_ITEMS):
    # transactions
    rows = []
    start = datetime.now() - timedelta(days=90)
    for _ in range(n_events):
        user_id = random.randint(1, n_users)
        item_id = random.randint(1, n_items)
        action = random.choices(ACTIONS, weights=[70,20,7,3])[0]
        ts = start + timedelta(seconds=random.randint(0, 90*24*3600))
        price = round(random.uniform(5, 200), 2)
        rows.append((user_id, item_id, action, price, ts))
    df = pd.DataFrame(rows, columns=['user_id','item_id','action','price','created_at'])
    os.makedirs(os.path.dirname(out_tx), exist_ok=True)
    df.to_csv(out_tx, index=False)

    # items
    items = pd.DataFrame({
        'id': list(range(1, n_items+1)),
        'sku': [f"SKU{i:04d}" for i in range(1, n_items+1)],
        'title': [f"Item {i}" for i in range(1, n_items+1)],
        'category': ['category']*n_items
    })
    items.to_csv(out_items, index=False)
    print(f"Wrote {out_tx} and {out_items}")

if __name__ == "__main__":
    generate()

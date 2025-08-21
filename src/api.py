# src/api.py
from fastapi import FastAPI, HTTPException
from recommender import Recommender
from db import load_items, load_transactions

app = FastAPI(title="Ecom Recommender API")

_interactions = None
_items_df = None
try:
    _interactions = load_transactions(limit=100000)
except Exception:
    _interactions = None

try:
    _items_df = load_items()
except Exception:
    _items_df = None

rec = Recommender(items_df=_items_df, interactions_df=_interactions if _interactions is not None else None)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/recommend/{user_id}")
def recommend(user_id: int, n: int = 10):
    try:
        recs = rec.recommend(user_id, n)
        return {"user_id": user_id, "recommendations": recs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
def predict(user_item: dict):
    try:
        uid = user_item["user_id"]
        iid = user_item["item_id"]
        score = rec.predict(uid, iid)
        return {"user_id": uid, "item_id": iid, "score": float(score) if score is not None else None}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

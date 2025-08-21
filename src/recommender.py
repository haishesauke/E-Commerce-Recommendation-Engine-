# src/recommender.py
import joblib
import os
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'svd_model.pkl')
ITEMS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'items.csv')

class Recommender:
    def __init__(self, model_path=MODEL_PATH, items_df=None, interactions_df=None):
        self.model = joblib.load(model_path) if os.path.exists(model_path) else None

        if items_df is not None:
            self.items = items_df['id'].astype(str).tolist()
        else:
            try:
                items_df = pd.read_csv(ITEMS_PATH)
                self.items = items_df['id'].astype(str).tolist()
            except Exception:
                self.items = []

        self.interactions = interactions_df if interactions_df is not None else pd.DataFrame(columns=['user_id', 'item_id'])

        if len(self.interactions) > 0:
            self.popularity = (
                self.interactions.groupby('item_id').size().sort_values(ascending=False).index.astype(str).tolist()
            )
        else:
            self.popularity = self.items[:100]

    def _get_seen_items(self, user_id):
        if self.interactions is None or self.interactions.empty:
            return set()
        return set(
            self.interactions[self.interactions['user_id'].astype(str) == str(user_id)]['item_id'].astype(str).tolist()
        )

    def recommend(self, user_id, n=10):
        seen = self._get_seen_items(user_id)
        candidates = [iid for iid in self.items if iid not in seen]
        if not candidates or self.model is None:
            return [int(i) for i in self.popularity[:n]]

        preds = []
        for iid in candidates:
            est = self.model.predict(str(user_id), str(iid)).est
            preds.append((iid, est))
        preds.sort(key=lambda x: x[1], reverse=True)
        top = [int(iid) for iid, _ in preds[:n]]
        return top

    def predict(self, user_id, item_id):
        if self.model is None:
            return None
        return self.model.predict(str(user_id), str(item_id)).est

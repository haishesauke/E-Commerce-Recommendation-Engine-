# tests/test_recommender.py
from src.recommender import Recommender
import pandas as pd

def test_recommender_cold_start():
    items = pd.DataFrame({'id':[1,2,3,4]})
    rec = Recommender(items_df=items, interactions_df=pd.DataFrame())
    top = rec.recommend(user_id=12345, n=2)
    assert isinstance(top, list)

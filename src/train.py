# src/train.py
import pandas as pd
import joblib
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split, GridSearchCV
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_transactions.csv')
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'svd_model.pkl')

ACTION_WEIGHT = {
    'view': 1.0,
    'click': 2.0,
    'cart': 3.0,
    'purchase': 5.0
}

def build_interactions(df):
    df['weight'] = df['action'].map(ACTION_WEIGHT).fillna(0)
    agg = df.groupby(['user_id', 'item_id'])['weight'].sum().reset_index()
    min_w, max_w = agg['weight'].min(), agg['weight'].max()
    if max_w == min_w:
        agg['rating'] = 3.0
    else:
        agg['rating'] = 1.0 + 4.0 * (agg['weight'] - min_w) / (max_w - min_w)
    return agg[['user_id', 'item_id', 'rating']]

def train():
    df = pd.read_csv(DATA_PATH)
    interactions = build_interactions(df)
    reader = Reader(rating_scale=(1.0, 5.0))
    data = Dataset.load_from_df(interactions[['user_id', 'item_id', 'rating']], reader)
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

    param_grid = {
        'n_factors': [50, 100],
        'lr_all': [0.002, 0.005],
        'reg_all': [0.02, 0.05]
    }
    gs = GridSearchCV(SVD, param_grid, measures=['rmse'], cv=3, n_jobs=-1)
    gs.fit(data)
    best_params = gs.best_params['rmse']
    print("Best params:", best_params)

    algo = SVD(**best_params)
    algo.fit(trainset)

    preds = algo.test(testset)
    from surprise import accuracy
    rmse = accuracy.rmse(preds)
    print("Test RMSE:", rmse)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(algo, MODEL_PATH)
    print("Model saved to", MODEL_PATH)

if __name__ == "__main__":
    train()

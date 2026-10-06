"""Train the house price model and save it as house_price_model.pkl.

Uses a synthetic dataset by default. To use real data, put a CSV named
housing.csv in this folder with columns:
area, bedrooms, bathrooms, location, price
"""
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

HERE = Path(__file__).resolve().parent
CSV = HERE / "housing.csv"

# approximate price per sq.ft (INR) used only for synthetic data
RATES = {"Indore": 4300, "Bhopal": 3800, "Mumbai": 18000, "Delhi": 11000,
         "Pune": 7500, "Bangalore": 8500, "Ahmedabad": 5000, "Jaipur": 4500}


def make_synthetic(n=4000, seed=42):
    rng = np.random.default_rng(seed)
    loc = rng.choice(list(RATES), n)
    area = rng.integers(500, 4000, n)
    bed = np.clip((area / 600 + rng.integers(-1, 2, n)).round().astype(int), 1, 6)
    bath = np.clip(bed - rng.integers(0, 2, n), 1, 5)
    rate = np.array([RATES[l] for l in loc])
    price = area * rate * rng.normal(1, 0.08, n) + bed * 150000 + bath * 100000
    return pd.DataFrame({"area": area, "bedrooms": bed, "bathrooms": bath,
                         "location": loc, "price": price.round(-3)})


df = pd.read_csv(CSV) if CSV.exists() else make_synthetic()
X, y = df[["area", "bedrooms", "bathrooms", "location"]], df["price"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

pre = ColumnTransformer(
    [("loc", OneHotEncoder(handle_unknown="ignore"), ["location"])],
    remainder="passthrough")
model = Pipeline([("pre", pre),
                  ("rf", RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1))])
model.fit(X_tr, y_tr)
pred = model.predict(X_te)
print(f"R2: {r2_score(y_te, pred):.3f} | MAE: Rs {mean_absolute_error(y_te, pred):,.0f}")
joblib.dump(model, HERE / "house_price_model.pkl")
print("Saved house_price_model.pkl")

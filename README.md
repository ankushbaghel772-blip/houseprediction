# House Price Prediction (Django + scikit-learn)

## Setup
    python -m venv venv
    venv\Scripts\activate          # Windows  (Linux/Mac: source venv/bin/activate)
    pip install -r requirements.txt
    python ml_model/train_model.py # creates ml_model/house_price_model.pkl
    python manage.py makemigrations prediction
    python manage.py migrate
    python manage.py createsuperuser   # optional, for /admin
    python manage.py runserver

Open http://127.0.0.1:8000/

## Using real data
Put `housing.csv` (columns: area, bedrooms, bathrooms, location, price) in `ml_model/`,
add your cities to `LOCATIONS` in `prediction/forms.py`, then re-run `train_model.py`.

## MySQL/PostgreSQL
Change `DATABASES` in `house_prediction/settings.py` (and `pip install mysqlclient` / `psycopg2-binary`).

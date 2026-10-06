from pathlib import Path

import joblib
import pandas as pd
from django.conf import settings
from django.shortcuts import render

from .forms import PredictionForm
from .models import HousePrediction

MODEL_PATH = Path(settings.BASE_DIR) / "ml_model" / "house_price_model.pkl"
_model = None


def get_model():
    """Load the model once and reuse it."""
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def format_inr(value):
    """Format a number in Indian style, e.g. 6500000 -> 65,00,000."""
    s = str(int(round(value)))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts + [tail])


def home(request):
    form = PredictionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        features = pd.DataFrame([{
            "area": d["area"], "bedrooms": d["bedrooms"],
            "bathrooms": d["bathrooms"], "location": d["location"]}])
        price = float(get_model().predict(features)[0])
        HousePrediction.objects.create(predicted_price=price, **d)
        return render(request, "prediction/result.html",
                      {"data": d, "price": format_inr(price)})
    return render(request, "prediction/home.html", {"form": form})


def history(request):
    items = HousePrediction.objects.all()[:50]
    for i in items:
        i.price_fmt = format_inr(i.predicted_price)
    return render(request, "prediction/history.html", {"items": items})

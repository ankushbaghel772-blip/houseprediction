from django import forms

LOCATIONS = ["Indore", "Bhopal", "Mumbai", "Delhi", "Pune",
             "Bangalore", "Ahmedabad", "Jaipur"]


class PredictionForm(forms.Form):
    area = forms.FloatField(label="Area (sq.ft)", min_value=100, max_value=20000)
    bedrooms = forms.IntegerField(min_value=1, max_value=10)
    bathrooms = forms.IntegerField(min_value=1, max_value=10)
    location = forms.ChoiceField(choices=[(l, l) for l in LOCATIONS])

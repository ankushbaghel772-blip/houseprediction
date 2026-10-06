from django.contrib import admin
from .models import HousePrediction


@admin.register(HousePrediction)
class HousePredictionAdmin(admin.ModelAdmin):
    list_display = ("location", "area", "bedrooms", "bathrooms",
                    "predicted_price", "created_at")
    list_filter = ("location",)

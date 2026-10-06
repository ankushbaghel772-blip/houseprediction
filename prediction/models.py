from django.db import models


class HousePrediction(models.Model):
    area = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    location = models.CharField(max_length=100)
    predicted_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.location} - {self.area} sq.ft - Rs {self.predicted_price:,.0f}"

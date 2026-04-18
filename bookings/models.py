from django.db import models

class MasterBooking(models.Model):
    TYPES = [('FLIGHT', 'Flight'), ('TRAIN', 'Train'), ('MOVIE', 'Movie'), ('CAFE', 'Cafe')]
    category = models.CharField(max_length=10, choices=TYPES)
    customer_name = models.CharField(max_length=100)
    details = models.TextField() # e.g., "Seat A1" or "Chicken Pizza"
    total_bill = models.FloatField()
    is_delivery = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.category}"
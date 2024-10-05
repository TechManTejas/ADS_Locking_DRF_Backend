from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField()

    def __str__(self):
        return self.flight_number
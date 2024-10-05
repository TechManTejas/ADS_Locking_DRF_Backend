from django.db import models
from flight.models import Flight


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    seat_number = models.IntegerField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.passenger_name} - {self.seat_number}'
from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.flight_number} from {self.departure_city} to {self.arrival_city}"

class Seat(models.Model):
    flight = models.ForeignKey(Flight, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    is_locked = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat_number} on flight {self.flight.flight_number}"

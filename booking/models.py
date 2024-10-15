from django.db import models
from flight.models import Flight, Seat


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')
    passenger_name = models.CharField(max_length=100)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.passenger_name} - Seat {self.seat.seat_number} on Flight {self.flight.flight_number}'

from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField()

    def __str__(self):
        return self.flight_number
    

class Seat(models.Model):
    flight = models.ForeignKey(Flight, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    class_type = models.CharField(max_length=10, choices=[('Economy', 'Economy'), ('Business', 'Business')], default='Economy')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Seat {self.seat_number} on Flight {self.flight.flight_number}"
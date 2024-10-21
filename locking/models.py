from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from flight.models import Seat

class SeatLock(models.Model):
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locked_at = models.DateTimeField(auto_now_add=True)
    lock_expires_at = models.DateTimeField()

    def is_lock_expired(self):
        return timezone.now() > self.lock_expires_at

    def __str__(self):
        return f"Lock for {self.seat.seat_number}"

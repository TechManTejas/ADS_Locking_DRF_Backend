from django.db import models
from django.utils import timezone
from django.db import transaction
from flight.models import Seat

class Lock(models.Model):
    LOCK_TYPES = [
        ('SHARED', 'Shared'),
        ('EXCLUSIVE', 'Exclusive')
    ]
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='locks')
    lock_type = models.CharField(choices=LOCK_TYPES, max_length=10)
    transaction_id = models.IntegerField()  # Transaction holding this lock
    acquired_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMMITTED', 'Committed'),
        ('ABORTED', 'Aborted')
    ]
    transaction_id = models.AutoField(primary_key=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='ACTIVE')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    @transaction.atomic
    def acquire_lock(self, seat, lock_type):
        """
        Acquires a lock on the given seat if it's not already locked or booked.
        Ensures atomicity and concurrency control with database-level row locking.
        """
        seat = Seat.objects.select_for_update().get(id=seat.id)

        if not seat.is_available:
            raise Exception(f"Seat {seat.seat_number} is already booked and cannot be locked.")

        current_locks = Lock.objects.filter(seat=seat)

        if lock_type == 'EXCLUSIVE':
            if current_locks.exists():
                raise Exception(f"Seat {seat.seat_number} is already locked by another transaction.")
            Lock.objects.create(transaction_id=self.transaction_id, seat=seat, lock_type=lock_type)
            seat.is_available = False  # Temporarily mark seat as unavailable
            seat.save()

        elif lock_type == 'SHARED':
            if current_locks.filter(lock_type='EXCLUSIVE').exists():
                raise Exception(f"Exclusive lock exists on seat {seat.seat_number}. Cannot acquire shared lock.")
            Lock.objects.create(transaction_id=self.transaction_id, seat=seat, lock_type=lock_type)

    @transaction.atomic
    def commit(self):
        """
        Commit the transaction by marking it as committed and releasing all locks.
        """
        self.status = 'COMMITTED'
        self.end_time = timezone.now()
        self.save()

        # Mark seats associated with this transaction as permanently unavailable (booked)
        locks = Lock.objects.filter(transaction_id=self.transaction_id)
        for lock in locks:
            seat = lock.seat
            seat.is_available = False  # Seat now permanently unavailable (booked)
            seat.save()

        # Delete all locks associated with this transaction after commit
        locks.delete()

    @transaction.atomic
    def abort(self):
        """
        Abort the transaction by marking it as aborted and releasing all locks.
        """
        self.status = 'ABORTED'
        self.end_time = timezone.now()
        self.save()

        # Make seats available again after abort
        locks = Lock.objects.filter(transaction_id=self.transaction_id)
        for lock in locks:
            seat = lock.seat
            seat.is_available = True  # Seat becomes available again
            seat.save()

        # Delete all locks associated with this transaction after abort
        locks.delete()

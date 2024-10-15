from django.db import models
from django.utils import timezone

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

    def acquire_lock(self, resource, lock_type):
        """
        Acquires a lock on the given resource (could be a flight or seat).
        Checks for conflicting locks before acquiring a new one.
        """
        current_locks = Lock.objects.filter(resource=resource)

        # For exclusive lock, ensure no other locks (shared/exclusive) exist
        if lock_type == 'EXCLUSIVE':
            if current_locks.exists():
                raise Exception(f"Resource {resource} is already locked by another transaction")

        # For shared lock, ensure no exclusive locks exist
        elif lock_type == 'SHARED':
            if current_locks.filter(lock_type='EXCLUSIVE').exists():
                raise Exception(f"Exclusive lock exists on resource {resource}")

        # If no conflict, acquire lock
        Lock.objects.create(transaction_id=self.transaction_id, resource=resource, lock_type=lock_type)

    def release_locks(self):
        """
        Releases all locks held by this transaction.
        """
        Lock.objects.filter(transaction_id=self.transaction_id).delete()

    def commit(self):
        """
        Commit the transaction by marking it as committed and releasing all locks.
        """
        self.status = 'COMMITTED'
        self.end_time = timezone.now()
        self.save()
        self.release_locks()

    def abort(self):
        """
        Abort the transaction by marking it as aborted and releasing all locks.
        """
        self.status = 'ABORTED'
        self.end_time = timezone.now()
        self.save()
        self.release_locks()

    def detect_deadlock(self):
        """
        Placeholder for deadlock detection logic.
        """
        pass

    def __str__(self):
        return f'Transaction {self.transaction_id} - {self.status}'
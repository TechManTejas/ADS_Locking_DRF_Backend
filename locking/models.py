from django.db import models

class Lock(models.Model):
    LOCK_TYPES = [
        ('SHARED', 'Shared'),
        ('EXCLUSIVE', 'Exclusive')
    ]
    resource = models.CharField(max_length=100)  # Could be flight or seat representation
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
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def acquire_lock(self, flight, lock_type):
        current_locks = Lock.objects.filter(resource=flight.flight_number)

        if lock_type == 'EXCLUSIVE':
            # Ensure no shared/exclusive lock exists for this flight/seat
            if current_locks.exists():
                raise Exception("Flight is already locked by another transaction")
        elif lock_type == 'SHARED':
            # Allow shared locks but block if exclusive lock exists
            if current_locks.filter(lock_type='EXCLUSIVE').exists():
                raise Exception("Exclusive lock exists on this flight")

        # No conflicts, acquire lock
        Lock.objects.create(transaction_id=self.transaction_id, resource=flight.flight_number, lock_type=lock_type)

    def release_locks(self):
        # Release all locks held by this transaction
        Lock.objects.filter(transaction_id=self.transaction_id).delete()

    def detect_deadlock(self):
        # Simplified logic for detecting deadlocks
        pass

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Transaction, Lock, Seat
from .serializers import TransactionSerializer, LockSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=True, methods=["post"], url_path="acquire-lock")
    def acquire_lock(self, request, pk=None):
        transaction = self.get_object()
        seat_id = request.data.get("seat_id")
        lock_type = request.data.get("lock_type")
        seat = Seat.objects.get(id=seat_id)

        # Check if seat already has an exclusive lock
        existing_locks = Lock.objects.filter(seat=seat)

        # Exclusive lock check
        if existing_locks.filter(lock_type="EXCLUSIVE").exists():
            return Response(
                {"error": "Seat is already exclusively locked by another transaction."},
                status=400,
            )

        # Shared lock check (for other transactions)
        if lock_type == "EXCLUSIVE" and existing_locks.exists():
            return Response(
                {"error": "Seat has shared locks, cannot acquire an exclusive lock."},
                status=400,
            )

        # Proceed to acquire the lock if no conflicts
        try:
            transaction.acquire_lock(seat, lock_type)
            return Response({"message": "Lock acquired successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @action(detail=True, methods=["post"])
    def commit(self, request, pk=None):
        transaction = self.get_object()
        transaction.commit()
        return Response({"message": "Transaction committed successfully"})

    @action(detail=True, methods=["post"])
    def abort(self, request, pk=None):
        transaction = self.get_object()
        transaction.abort()
        return Response({"message": "Transaction aborted"})


class LockViewSet(viewsets.ModelViewSet):
    queryset = Lock.objects.all()
    serializer_class = LockSerializer

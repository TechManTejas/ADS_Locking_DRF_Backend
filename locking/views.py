from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Transaction, Lock, Seat
from .serializers import TransactionSerializer, LockSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=True, methods=['post'])
    def acquire_lock(self, request, pk=None):
        transaction = self.get_object()
        seat_id = request.data.get('seat_id')
        lock_type = request.data.get('lock_type')
        seat = Seat.objects.get(id=seat_id)
        try:
            transaction.acquire_lock(seat, lock_type)
            return Response({'message': 'Lock acquired successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=True, methods=['post'])
    def commit(self, request, pk=None):
        transaction = self.get_object()
        transaction.commit()
        return Response({'message': 'Transaction committed successfully'})

    @action(detail=True, methods=['post'])
    def abort(self, request, pk=None):
        transaction = self.get_object()
        transaction.abort()
        return Response({'message': 'Transaction aborted'})

class LockViewSet(viewsets.ModelViewSet):
    queryset = Lock.objects.all()
    serializer_class = LockSerializer
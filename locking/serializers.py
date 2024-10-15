from rest_framework import serializers
from .models import Transaction, Lock

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'status', 'start_time', 'end_time']

class LockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lock
        fields = ['id', 'resource', 'lock_type', 'transaction', 'acquired_at']
from rest_framework import serializers
from .models import  Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'seat', 'passenger_name', 'booked_at']

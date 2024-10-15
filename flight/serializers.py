from rest_framework import serializers
from .models import Flight, Seat

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'is_available', 'flight']


class FlightSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True)

    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'departure_time', 'available_seats', 'seats']



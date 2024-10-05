from rest_framework import viewsets, status
from rest_framework.response import Response

from booking.models import Booking
from flight.models import Flight
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create_booking(self, request):
        flight_id = request.data.get("flight_id")
        passenger_name = request.data.get("passenger_name")
        seat_number = request.data.get("seat_number")

        try:
            # Start a new transaction
            transaction = Transaction.objects.create(status="ACTIVE")

            # Fetch the flight
            flight = Flight.objects.get(id=flight_id)

            # Acquire exclusive lock for seat booking
            transaction.acquire_lock(flight, "EXCLUSIVE")

            # Create booking
            Booking.objects.create(
                flight=flight, passenger_name=passenger_name, seat_number=seat_number
            )

            # Commit transaction
            transaction.status = "COMMITTED"
            transaction.release_locks()
            transaction.save()

            return Response(
                {"status": "Booking successful"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            # Handle failure and rollback
            transaction.status = "ABORTED"
            transaction.release_locks()
            transaction.save()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

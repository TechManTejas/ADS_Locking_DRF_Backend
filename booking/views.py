from rest_framework import viewsets
from .models import Booking
from rest_framework.response import Response
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        seat_id = request.data.get('seat')
        seat = seat.objects.get(id=seat_id)

        # Check if the seat is available before creating a booking
        if not seat.is_available:
            return Response({'error': 'Seat is already booked'}, status=400)

        return super().create(request, *args, **kwargs)

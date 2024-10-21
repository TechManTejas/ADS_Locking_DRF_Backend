from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.http import JsonResponse
from flight.models import Seat
from locking.models import SeatLock
from .models import Booking

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_seat(request, seat_id):
    user = request.user
    try:
        with transaction.atomic():
            seat = Seat.objects.select_for_update().get(id=seat_id)

            # Check if the seat is locked
            if seat.is_locked:
                seat_lock = SeatLock.objects.get(seat=seat)
                
                # Check if the lock is expired
                if seat_lock.is_lock_expired():
                    # Unlock the seat if the lock is expired
                    seat.is_locked = False
                    seat.save()
                    seat_lock.delete()
                    return JsonResponse({'status': 'error', 'message': 'Seat lock expired. Try again.'}, status=400)
                
                # Only the user who locked the seat can book it
                if seat_lock.user != user:
                    return JsonResponse({'status': 'error', 'message': 'Seat locked by another user.'}, status=400)

                # Proceed with booking
                seat.is_booked = True
                seat.is_locked = False
                seat.save()
                seat_lock.delete()  # Remove the lock after booking
                Booking.objects.create(user=user, flight=seat.flight, seat=seat)

                return JsonResponse({'status': 'success', 'message': 'Seat booked successfully.'})
        
        return JsonResponse({'status': 'error', 'message': 'Seat is not locked or already booked.'}, status=400)
    
    except Seat.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Seat not found.'}, status=404)

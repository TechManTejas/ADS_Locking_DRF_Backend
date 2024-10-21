from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.http import JsonResponse
from flight.models import Seat
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import SeatLock

LOCK_DURATION = 1  # Lock expires after 15 minutes

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lock_seat(request, seat_id):
    user = request.user
    try:
        seat = Seat.objects.get(id=seat_id)

        # Check if the seat is already booked
        if seat.is_booked:
            return JsonResponse({'status': 'error', 'message': 'Seat already booked.'}, status=400)

        # Check if the seat is already locked and if the lock is expired
        if seat.is_locked:
            seat_lock = SeatLock.objects.get(seat=seat)
            if seat_lock.is_lock_expired():
                # If lock is expired, remove the lock
                seat.is_locked = False
                seat.save()
                seat_lock.delete()
            elif seat_lock.user != user:
                # If another user has the lock, prevent locking
                return JsonResponse({'status': 'error', 'message': 'Seat is locked by another user.'}, status=400)

        # Lock the seat for the current user
        seat.is_locked = True
        seat.save()
        lock_expires_at = timezone.now() + timezone.timedelta(minutes=LOCK_DURATION)
        SeatLock.objects.create(seat=seat, user=user, lock_expires_at=lock_expires_at)

        # Notify WebSocket group after locking seat
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'seat_locking',  # The group name
            {
                'type': 'seat_update',
                'message': {
                    'action': 'lock',
                    'seat_id': seat.id,
                }
            }
        )

        return JsonResponse({'status': 'success', 'message': 'Seat locked successfully.'})
    
    except Seat.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Seat not found.'}, status=404)

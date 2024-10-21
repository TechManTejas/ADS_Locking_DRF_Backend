from django.http import JsonResponse

from locking.models import SeatLock
from .models import Flight, Seat

def list_flights(request):
    flights = Flight.objects.all()
    flight_data = []
    
    for flight in flights:
        flight_data.append({
            'id': flight.id,
            'flight_number': flight.flight_number,
            'departure_city': flight.departure_city,
            'arrival_city': flight.arrival_city,
            'departure_time': flight.departure_time,
            'arrival_time': flight.arrival_time,
        })
    
    return JsonResponse({'flights': flight_data})

def list_seats(request, flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
        seats = flight.seats.all()
        seat_data = []
        
        for seat in seats:
            # Check if the seat is locked and if the lock is expired
            if seat.is_locked:
                try:
                    seat_lock = SeatLock.objects.get(seat=seat)
                    if seat_lock.is_lock_expired():
                        # If the lock is expired, unlock the seat and delete the lock
                        seat.is_locked = False
                        seat.save()
                        seat_lock.delete()  # Remove the expired lock
                except SeatLock.DoesNotExist:
                    # If no lock exists, ensure the seat is unlocked
                    seat.is_locked = False
                    seat.save()

            # Prepare seat data after checking the lock status
            seat_data.append({
                'id': seat.id,
                'seat_number': seat.seat_number,
                'is_locked': seat.is_locked,
                'is_booked': seat.is_booked
            })
        
        return JsonResponse({'seats': seat_data})
    
    except Flight.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Flight not found.'}, status=404)

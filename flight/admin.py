from django.contrib import admin
from .models import Flight, Seat

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0  # This removes the extra blank seat form fields by default


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'departure_city', 'arrival_city', 'departure_time', 'arrival_time')
    search_fields = ('flight_number', 'departure_city', 'arrival_city')
    list_filter = ('departure_city', 'arrival_city', 'departure_time')
    inlines = [SeatInline]  # Add the SeatInline here to display seats inline

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'flight', 'is_locked', 'is_booked')
    list_filter = ('flight', 'is_locked', 'is_booked')
    search_fields = ('seat_number', 'flight__flight_number')

from django.contrib import admin
from .models import Flight, Seat

# Inline model to display seats in the Flight admin page
class SeatInline(admin.TabularInline):
    model = Seat
    extra = 1  # Number of extra empty seat fields to display for easy addition

# Flight admin with seats inline
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'departure_time', 'available_seats')  # Display flight details
    inlines = [SeatInline]  # Add seats inline in flight admin

class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'flight', 'is_available')
    list_filter = ('flight', 'is_available')  # Allow filtering by flight and availability
    search_fields = ('seat_number', 'flight__flight_number')  # Search by seat number or flight number

admin.site.register(Seat, SeatAdmin)
admin.site.register(Flight, FlightAdmin)

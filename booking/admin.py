from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight', 'seat', 'booked_at')
    search_fields = ('user__username', 'flight__flight_number', 'seat__seat_number')
    list_filter = ('flight', 'booked_at')

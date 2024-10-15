from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('passenger_name', 'seat', 'booked_at')
    search_fields = ('passenger_name', 'seat__seat_number')
    list_filter = ('seat__flight',)  # Allow filtering by flight

admin.site.register(Booking, BookingAdmin)


from django.contrib import admin
from .models import SeatLock

@admin.register(SeatLock)
class SeatLockAdmin(admin.ModelAdmin):
    list_display = ('seat', 'user', 'locked_at', 'lock_expires_at')
    search_fields = ('seat__seat_number', 'user__username')
    list_filter = ('locked_at', 'lock_expires_at')

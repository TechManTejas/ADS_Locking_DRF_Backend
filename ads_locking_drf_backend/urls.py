from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('flight/', include('flight.urls')),  # Flight-related endpoints
    path('booking/', include('booking.urls')),  # Booking-related endpoints
    path('locking/', include('locking.urls')),  # Locking-related endpoints
    path('users/', include('users.urls')),  # User-related endpoints (registration, login)
]

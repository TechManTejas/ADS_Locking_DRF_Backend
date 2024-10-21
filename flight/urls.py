from django.urls import path
from . import views

urlpatterns = [
    path('flights/', views.list_flights, name='list_flights'),
    path('flights/<int:flight_id>/seats/', views.list_seats, name='list_seats'),
]

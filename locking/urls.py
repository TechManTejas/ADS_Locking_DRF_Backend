from django.urls import path
from . import views

urlpatterns = [
    path('lock/<int:seat_id>/', views.lock_seat, name='lock_seat'),
]
from django.urls import path

from . import views
from .views import read_cycle_file, update_schedule

urlpatterns = [
    path("", views.dashboard, name="templates/dashboard"),
    path('read_cycle_file/<str:device>/', read_cycle_file, name='read_cycle_file'),
    path('update_schedule/<str:device>/', update_schedule, name='update_schedule'),
]

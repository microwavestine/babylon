from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("farmdiary/", views.farmdiary, name="farmdiary"),
    path('read_cycle_file/<str:device>/', views.read_cycle_file, name='read_cycle_file'),
    path('update_schedule/<str:device>/', views.update_schedule, name='update_schedule'),
    path('farmdiary/<int:saved_data_id>/', views.farmdiary, name='farmdiary'),
    path('get_images_for_date/', views.get_images_for_date, name='get_images_for_date'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
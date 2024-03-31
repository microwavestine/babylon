from django.shortcuts import render
from django.http import HttpResponse
from .models import DataPoint

# Create your views here.
def dashboard(request):
    data_points = DataPoint.objects.all()
    return render(request, 'dashboard.html', {'data_points': data_points})

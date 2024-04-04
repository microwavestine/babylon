from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from .models import DataPoint
from django.http import JsonResponse

# Create your views here.
def dashboard(request):
    data_points = DataPoint.objects.all()
    return render(request, 'dashboard.html', {'data_points': data_points})

def read_cycle_file(request, device):
    try:
        with open(f'/home/pilab/Desktop/babylon/hanginggarden/scheduler/{device}_schedule.txt', 'r') as file:
            data = file.read()
        return HttpResponse(data, content_type='text/plain')
    except FileNotFoundError:
        return HttpResponseNotFound('File not found')
    except Exception as e:
        return HttpResponseServerError(str(e))
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from .models import DataPoint
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


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
    
@csrf_exempt
def update_schedule(request, device):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            hour = int(data.get('hour'))
            minute = int(data.get('minute'))
            status = data.get('status').upper()  # Ensure status is uppercase
            print(hour)
            print(minute)
            print(status)
            # Adjust for the 5-minute interval for the pump motor schedule
            minute = minute // 5 * 5  # Round down to the nearest 5-minute interval
            
            with open(f'/home/pilab/Desktop/babylon/hanginggarden/scheduler/{device}_schedule.txt', 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    time, current_status = line.strip().split(" ", 1)
                    # Adjust for the 5-minute interval for the pump motor schedule
                    schedule_hour, schedule_minute = map(str, time.split(':'))
                    #schedule_minute = int(schedule_minute) // 5 * 5
                    
                    if f"{hour:02d}" == schedule_hour and f"{minute:02d}" == schedule_minute:
                        new_status = 'ON' if status.upper() == 'OFF' else 'OFF'
                        print(f"{hour:02d}:{minute:02d} {new_status}\n")
                        file.write(f"{hour:02d}:{minute:02d} {new_status}\n")
                    else:
                        file.write(line)
                file.truncate()
                
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
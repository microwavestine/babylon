from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from .models import DataPoint
from django.http import JsonResponse
from .forms import SaveDataForm
from .models import SavedData, Image
from django.views.decorators.csrf import csrf_exempt
import json
import datetime


# Create your views here.
def dashboard(request):
    data_points = DataPoint.objects.all()
    return render(request, 'dashboard.html', {'data_points': data_points})

def farmdiary(request, saved_data_id=None):
    if saved_data_id:
        # Viewing an existing SavedData instance
        saved_data = get_object_or_404(SavedData, id=saved_data_id)
        images = saved_data.images.all()
        context = {
            'form': None,
            'saved_data': saved_data,
            'images': images,
        }
        return render(request, 'farmdiary.html', context)
    else:
        if request.method == 'POST':
            form = SaveDataForm(request.POST, request.FILES)
            if form.is_valid():
                date = form.cleaned_data['date']
                text = form.cleaned_data['text']
                button_choice = request.POST.get('button_choice')
                saved_data = SavedData.objects.create(date=date, text=text, button_choice=button_choice)
                print(f"Saved data instance: {saved_data}")
                print(f"Saved data text: {saved_data.text}")
                print(f"Button choice: {button_choice}")
                images = request.FILES.getlist('images')
                print(f"Images list: {images}")
                for image in images:
                    img = Image.objects.create(image=image)
                    saved_data.images.add(img)
                    print(f"Saved image: {img}")
                return redirect('farmdiary')
        else:
            form = SaveDataForm()
        return render(request, 'farmdiary.html', {'form': form})
    

def get_images_for_date(request):
    if request.method == 'GET':
        date_str = request.GET.get('date')
        if date_str:
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                saved_data = SavedData.objects.filter(date=date)
                image_urls = [image.image.url for data in saved_data for image in data.images.all()]
                print(image_urls)
                return JsonResponse({'success': True, 'image_urls': image_urls})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'No date provided'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    

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
                        # print(f"{hour:02d}:{minute:02d} {new_status}\n")
                        file.write(f"{hour:02d}:{minute:02d} {new_status}\n")
                    else:
                        file.write(line)
                file.truncate()
                
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    


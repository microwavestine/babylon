from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from .models import DataPoint
from django.http import JsonResponse
from .forms import SaveDataForm
from .models import SavedData, Image
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def dashboard(request):
    data_points = DataPoint.objects.all()
    return render(request, 'dashboard.html', {'data_points': data_points})

def farmdiary(request, saved_data_id=None):
    if saved_data_id:
        # Viewing and updating an existing SavedData instance
        saved_data = get_object_or_404(SavedData, id=saved_data_id)
        images = saved_data.images.all()

        if request.method == 'POST':
            form = SaveDataForm(request.POST, request.FILES, instance=saved_data)
            if form.is_valid():
                saved_data.text = form.cleaned_data['text']
                saved_data.button_choice = request.POST.get('button_choice')
                saved_data.save()

                # Handle new images
                images = request.FILES.getlist('images')
                for image in images:
                    img = Image.objects.create(image=image)
                    saved_data.images.add(img)

                return redirect('farmdiary', saved_data_id=saved_data.id)
        else:
            form = SaveDataForm(instance=saved_data)

        context = {
            'form': form,
            'saved_data': saved_data,
            'images': images,
        }
        return render(request, 'farmdiary.html', context)
    else:
        # Creating or updating a SavedData instance
        saved_data = None
        if request.method == 'POST':
            form = SaveDataForm(request.POST, request.FILES)
            if form.is_valid():
                date = form.cleaned_data['date']
                text = form.cleaned_data['text']
                button_choice = request.POST.get('button_choice')

                # Check if a SavedData instance already exists for the given date and button_choice
                try:
                    saved_data = SavedData.objects.get(date=date, button_choice=button_choice)
                except SavedData.DoesNotExist:
                    # Create a new SavedData instance
                    saved_data = SavedData.objects.create(date=date, text=text, button_choice=button_choice)

                # Update the SavedData instance with the new text
                saved_data.text = text

                # Handle new images
                images = request.FILES.getlist('images')
                for image in images:
                    img = Image.objects.create(image=image)
                    saved_data.images.add(img)

                saved_data.save()

                return redirect('farmdiary', saved_data_id=saved_data.id)
        else:
            form = SaveDataForm()
        return render(request, 'farmdiary.html', {'form': form})
    
def get_images_for_date(request):
    if request.method == 'GET':
        date_str = request.GET.get('date')
        button_choice = request.GET.get('button_choice')
        if date_str and button_choice:
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                saved_data = SavedData.objects.filter(date=date, button_choice=button_choice)
                image_urls = [image.image.url for data in saved_data for image in data.images.all()]
                text_data = [data.text for data in saved_data]
                return JsonResponse({'success': True, 'image_urls': image_urls, 'text_data': text_data})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'No date or button choice provided'})
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
    


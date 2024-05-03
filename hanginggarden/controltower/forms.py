from django import forms
from .fields import MultiFileField
from .widgets import MultiFileInput
from django.utils import timezone
from django.db import models

class SaveDataForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control datetimepicker-input'}),
        initial=timezone.now()
    )
    text = forms.CharField(widget=forms.Textarea)
    button_choice = models.CharField(max_length=100, blank=True)
    images = MultiFileField(widget=MultiFileInput, required=False)
from django import forms
from .widgets import MultiFileInput

class MultiFileField(forms.FileField):
    widget = MultiFileInput
    default_error_messages = {
        'invalid': 'No file was submitted. Check the encoding type on the form.',
        'invalid_image': "Upload a valid image. The file you uploaded was either not an image or a corrupted image.",
    }

    def to_python(self, data):
        ret = []
        for item in data:
            try:
                ret.append(forms.FileField.to_python(self, item))
            except forms.ValidationError:
                raise forms.ValidationError(self.error_messages['invalid_image'])
        return ret
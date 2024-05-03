from django import forms
from django.utils.safestring import mark_safe

class MultiFileInput(forms.Widget):
    input_type = 'file'

    def __init__(self, attrs=None):
        default_attrs = {
            'multiple': True,
        }
        if attrs:
            attrs.update(default_attrs)
        else:
            attrs = default_attrs
        super().__init__(attrs=attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        else:
            return None

    def render(self, name, value, attrs=None, renderer=None):
        attrs = self.build_attrs(self.attrs, attrs)
        attrs_str = ' '.join([f'{key}="{value}"' for key, value in attrs.items()])
        return mark_safe(f'<input type="file" name="{name}" {attrs_str}>')
from django.forms import ModelForm
from .models import Cake


class CakeForm(ModelForm):
    class Meta:
        model = Cake
        exclude = ('baker',)

    def __init__(self, *args, **kwargs):
        super(CakeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'
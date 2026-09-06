from django import forms
from django.forms import ModelForm
from .models import Appointment
# Define your forms here.
class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        exclude = ('responsible_doctor', 'appointment_type')

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
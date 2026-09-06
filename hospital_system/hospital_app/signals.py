# Define your signal receivers here.
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete
from .models import Appointment, Doctor, Patient
from django.utils.timezone import now


@receiver(pre_save, sender=Appointment)
def appointment_status(sender, instance: Appointment, **kwargs):
    if instance.status == 'completed' and instance.datetime > now():
        instance.status = 'scheduled'
    if instance.status == 'scheduled' and instance.datetime < now():
        instance.status = 'completed'

    if instance.pk is None and instance.patient_id is not None:
        doctor = instance.responsible_doctor
        patient_institution = instance.patient.institution

        patient_ids = (Appointment.objects
         .filter(responsible_doctor=doctor, patient__institution=patient_institution)
         .values_list('patient_id', flat=True).distinct())

        if len(patient_ids) >= 3:
            instance.note = f"High workload with patients from institution {patient_institution}"

@receiver(pre_delete, sender=Patient)
def cleanup_patient_appointments(sender, instance: Patient, **kwargs):
    appointments = Appointment.objects.filter(patient=instance)
    for appointment in appointments:
        if appointment.status == 'scheduled':
            appointment.delete()
        elif appointment.status == 'in_progress':
            appointment.note = 'Patient record missing – appointment preserved for audit purposes'
            appointment.save()
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
    # Секој лекар се карактеризира со име и презиме (full_name), специјалност (кардиолог, дерматолог или невролог),
    # слика, институција од која доаѓа, број на успешно извршени прегледи, контакт е-пошта и телефон
    SPECIALTY_CHOICES = [
        ("cardiologist", "Cardiologist"),
        ("dermatologist", "Dermatologist"),
        ("neurologist", "Neurologist")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    specialty = models.CharField(choices=SPECIALTY_CHOICES, max_length=30)
    image = models.ImageField(upload_to="doctors/", null=True, blank=True)
    institution = models.CharField(max_length=100)
    completed_appointments = models.IntegerField(default=0)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name

# Секој пациент се карактеризира со име и презиме, датум на раѓање, пол и е-пошта за контакт.

class Patient(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female")
    ]
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    email = models.EmailField()
    institution = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


# Секој преглед се карактеризира со тип на преглед (кардиолошки, дерматолошки или невролошки),
# опис на симптоми, статус (закажан, во тек, завршен), термин (датум и време), и забелешка


class Appointment(models.Model):
    TYPE_CHOICES = [
        ("cardiologist", "Cardiologist"),
        ("dermatologist", "Dermatologist"),
        ("neurologist", "Neurologist")
    ]

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("in_progress", "In Progress"),
        ("completed", "Completed")
    ]

    appointment_type = models.CharField(choices=TYPE_CHOICES, max_length=20)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='scheduled')
    datetime = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    responsible_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='responsible_appointments')
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.appointment_type} - {self.datetime}"


class AppointmentAssignment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('appointment', 'doctor')

    def __str__(self):
        return f"{self.doctor.full_name} working on {self.appointment}"

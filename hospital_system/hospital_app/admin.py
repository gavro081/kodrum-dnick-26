from django.contrib import admin
from .models import Patient, Doctor, Appointment
from django.db.models import Q

# Register your models here.
# --- Лекари и пациенти може да бидат додадени само од супер-корисници.
# --- Прегледите може да бидат додадени од сите корисници - лекари, но корисникот што го додава прегледот автоматски станува одговорен лекар.
# --- Прегледите може да се менуваат само од лекар што е одговорен за нив или од супер-корисник
# --- Преглед може да се избрише само ако е незапочнат
# --- Кога прегледот во тек ќе премине во статус завршен, потребно е само одговорниот лекар да го инкрементира бројот на успешно завршени прегледи.
# --- Лекарите може да ги гледаат само прегледите на кои тие се одговорни или се доделени како асистенти

class DoctorAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

class PatientAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

class AppointmentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return Doctor.objects.filter(user=request.user).exists() or request.user.is_superuser

    def save_model(self, request, obj: Appointment, form, change):
        if not change:
            doctor = Doctor.objects.filter(user=request.user).first()
            if doctor:
                obj.responsible_doctor = doctor
        else:
            if obj.status == 'completed':
                obj.responsible_doctor.completed_appointments += 1
                obj.responsible_doctor.save()

        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj: Appointment = None):
        if request.user.is_superuser:
            return True

        doctor = Doctor.objects.filter(user=request.user).first()
        if doctor and obj.responsible_doctor == doctor:
                return True
        return False

    def has_delete_permission(self, request, obj:Appointment = None):
        if obj.status != 'scheduled':
            return False
        return True

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        doctor = Doctor.objects.filter(user=request.user).first()
        if not doctor:
            return qs.none()

        return qs.filter(Q(responsible_doctor=doctor) | Q(appointmentassignment__doctor=doctor))

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
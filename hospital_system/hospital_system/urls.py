"""
URL configuration for hospital_system project.
"""
from django.contrib import admin
from django.urls import path
from hospital_app import views as hospital_views
from hospital_system import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', hospital_views.index, name='index'),
    path('test/', hospital_views.test, name='test'),
    path("doctors/<int:doctor_id>/", hospital_views.doctor_detail, name='doctor_detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
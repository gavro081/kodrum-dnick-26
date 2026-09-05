import random

from django.contrib import admin
from django.core.exceptions import ValidationError

# Register your models here.
from .models import Cake, Baker

# --- Пекарите можат да бидат додадени, менувани и бришени само од супер-корисници.
# --- Еден пекар може да има максимум 10 торти во дадено време.
# --- Кога се брише пекарот, неговите торти по случаен избор се додаваат на останатите пекари.
# --- Вкупната цена на тортите на еден пекар не смее да надминува 10 000.
# --- Тортите можат да бидат менувани само од пекарите кои ги додале, а останатите пекари може само да ги гледаат тие торти.
# --- Пекар не може да додаде торта, ако веќе постои торта со истото име.
# --- На супер-корисниците во Админ панелот им се прикажуваат пекарите со помалку од 5 торти.

class BakerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        # return request.user.is_superuser
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            items = [item for item in queryset if item.cake_set.count() < 5]
            return items
        return queryset

    def delete_model(self, request, obj: Baker):
        bakers = list(Baker.objects.exclude(id=obj.id))
        cakes = obj.cake_set.all()
        for cake in cakes:
            cake.baker = random.choice(bakers)
            cake.save()

        super().delete_model(request, obj)

class CakeAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj = None):
        if request.user is not None:
            return True
        return False

    def has_change_permission(self, request, obj: Cake=None):
        if obj is not None and obj.baker.user == request.user:
            return True
        return False
        # return obj and obj.baker.user == request.user

    def save_model(self, request, obj: Cake, form, change):
        if not request.user.is_superuser:
            obj.baker = Baker.objects.get(user=request.user)

        cake_baker = obj.baker
        cakes = Cake.objects.filter(baker=cake_baker).exclude(id=obj.id)
        if cakes.count() >= 10:
            raise ValidationError('cannot more than 10 cakes per baker')

        total_price = 0
        for cake in cakes:
            total_price += cake.price

        if total_price + obj.price > 10000:
            raise ValidationError('cannot have sum of all cakes bigger than 10.000')

        return super().save_model(request, obj, form, change)

admin.site.register(Cake, CakeAdmin)
admin.site.register(Baker, BakerAdmin)
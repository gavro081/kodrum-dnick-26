from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Baker(models.Model):
    # име, презиме, телефон за контакт и email адреса
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Cake(models.Model):
    # име, цена, тежина, опис и слика
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    weight = models.IntegerField()
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cakes/', null=True, blank=True)
    baker = models.ForeignKey(Baker, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.price}"
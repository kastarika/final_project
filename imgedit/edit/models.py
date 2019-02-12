from django.db import models

# Create your models here.
class aks(models.Model):
    img = models.ImageField(default='', blank=True)
    show = models.BooleanField(default=False)

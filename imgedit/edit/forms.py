from django import forms
from . import models

class get_image(forms.ModelForm):
    class Meta:
        model = models.aks
        fields = ['img']

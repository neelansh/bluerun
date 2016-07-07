from django.db import models
from django.utils import timezone
from django import forms

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    contact=models.CharField(max_length=10, default =' ')
    subject=models.CharField(max_length=200, blank=True, null=True)  
    message=models.TextField(max_length=300, blank=True, null=True)
    datetime=models.DateTimeField(default = timezone.now)
    def __str__(self):
        return self.name

class ContactForm(forms.ModelForm):
    contact = forms.CharField(max_length=10, min_length=10)
    class Meta:
        model = Contact
        exclude = ['datetime']

        def __str__(self):
            return self.name
       

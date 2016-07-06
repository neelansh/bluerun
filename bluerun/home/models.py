from django.db import models
from django.utils import timezone
from django import forms

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    subject=models.CharField(max_length=200)  
    message=models.TextField(max_length=300,default=" ")
    def __str__(self):
        return self.name

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        def __str__(self):
            return self.name
       

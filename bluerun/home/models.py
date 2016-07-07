from django.db import models
from django.utils import timezone


# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=100)
<<<<<<< HEAD
    email=models.EmailField()
    contact=models.CharField(max_length=10, default =' ')
=======
    email=models.CharField(max_length=100)
    contact=models.CharField(max_length=10, default ='')
>>>>>>> dc9dd6923063cfbb075444aad60959bcf99025ae
    subject=models.CharField(max_length=200, blank=True, null=True)  
    message=models.TextField(max_length=300, blank=True, null=True)
    datetime=models.DateTimeField(default = timezone.now)
    def __str__(self):
        return '  '.join([
            self.name,
            self.email,
            self.contact,
        ])


<<<<<<< HEAD
=======
    def __str__(self):
        return self.name
>>>>>>> dc9dd6923063cfbb075444aad60959bcf99025ae
       

from django.db import models
from django.utils import timezone


# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=100)
<<<<<<< HEAD
    email=models.EmailField()
    contact=models.CharField(max_length=10, default ='')
=======
    email=models.EmailField(blank=True , null = True)
    contact=models.CharField(max_length=13)
>>>>>>> 8addc9d5f42936d53044f96563fffc9a5437ebf2
    subject=models.CharField(max_length=200, blank=True, null=True)  
    message=models.TextField(max_length=300, blank=True, null=True)
    datetime=models.DateTimeField(auto_now_add = True)

<<<<<<< HEAD

   

       
=======
    def __str__(self):
        return self.name
>>>>>>> 8addc9d5f42936d53044f96563fffc9a5437ebf2

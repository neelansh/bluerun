from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    contact = forms.CharField(max_length = 13 , min_length=10)
    class Meta:
        model = Contact
        exclude = ['datetime']
<<<<<<< HEAD

       
=======
>>>>>>> 8addc9d5f42936d53044f96563fffc9a5437ebf2

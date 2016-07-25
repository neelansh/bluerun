from django import forms
from account.models import MyUser

class EditProfileForm(forms.Form):
	email = forms.CharField(max_length=254, required = False)
	phone = forms.CharField(max_length = 10, required = False)
	first_name = forms.CharField(max_length = 30, required = False)
	last_name = forms.CharField(max_length = 30, required = False)
	
	def clean(self):
		email = self.cleaned_data.get('email', '')
		first_name = self.cleaned_data.get('first_name', '')
		last_name = self.cleaned_data.get('last_name','')
		phone = self.cleaned_data.get('phone','')
		return self.cleaned_data;
	class Meta:
		model = MyUser
		fields = ['email','phone', 'first_name', 'last_name']
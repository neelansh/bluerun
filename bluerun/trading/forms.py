from django import forms
from account.models import MyUser

class EditProfileForm(forms.ModelForm):
	email = forms.CharField(max_length=254, required = False)
	phone = forms.CharField(max_length = 10, required = False)
	first_name = forms.CharField(max_length = 30, required = False)
	last_name = forms.CharField(max_length = 30, required = False)


	def clean_email(self):
		data_email = self.cleaned_data['email']
		if (MyUser.objects.filter(email = data_email).exists()):
			raise forms.ValidationError('User with this email already exists.')
		return data_email

	class Meta:
		model = MyUser
		fields = ['email','phone', 'first_name', 'last_name']
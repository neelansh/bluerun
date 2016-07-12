from django import forms
from .models import MyUser
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 25);
    password = forms.CharField(widget = forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.authenticated_user = None;
        super(LoginForm, self).__init__(*args, **kwargs)
    
    def clean_username(self):
        data_username = self.cleaned_data['username']
        if MyUser.objects.filter(username = data_username).count() != 1:
            raise forms.ValidationError('Invalid Username')
        return data_username

    def clean(self):
        data_username = self.cleaned_data.get('username', '')
        data_passwd = self.cleaned_data.get('password', '')
        user = authenticate(username=data_username, password = data_passwd)
        if data_username and data_passwd and user is None:
            raise forms.ValidationError('Username/Password doesnot match')
        if user and user.is_active == False:
            raise forms.ValidationError('Inactive User')
        self.authenticated_user = user
        return self.cleaned_data;

class ResetPasswordForm(forms.Form):
    current_password = forms.CharField(widget = forms.PasswordInput)
    new_password = forms.CharField(widget = forms.PasswordInput)
    confirm_new_password = forms.CharField(widget = forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ResetPasswordForm , self).__init__(*args , **kwargs)

    def clean_current_password(self):
        password = self.cleaned_data.get('current_password' , '')
        if(password and not self.user.check_password(password)):
            raise forms.ValidationError('current password is wrong')
        return password

    def clean(self):
        password = self.cleaned_data.get('new_password' , '')
        confirm_password = self.cleaned_data.get('confirm_new_password' , '')
        if(password and confirm_password and password != confirm_password):
            raise forms.ValidationError('password and confirm password do not match')
        user = self.user
        return self.cleaned_data

class ForgotPassword(forms.Form):
    username = forms.CharField(max_length = 100)

    def clean_username(self):
        data_username = self.cleaned_data.get('username', '')
        if data_username and not MyUser.objects.filter(username = data_username).exists():
            raise forms.ValidationError('Invalid Username')
        return data_username

class SetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        data_new_password = self.cleaned_data.get('new_password')
        data_confirm_password = self.cleaned_data.get('confirm_password')
        if (data_new_password and data_confirm_password 
                and data_new_password != data_confirm_password):
            raise forms.ValidationError("The two passwords field didn't match")
        return data_confirm_password


class SignupForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def clean_email(self):
        data_email = self.cleaned_data.get('email', '')
        if not data_email:
            raise forms.ValidationError('This field is required')
        if MyUser.objects.filter(email = data_email).exists():
            raise forms.ValidationError('User with this email already exist')
        return data_email

    def clean_confirm_password(self):
        data_password = self.cleaned_data.get('password')
        data_confirm_password = self.cleaned_data.get('confirm_password')
        if (data_password and data_confirm_password 
                and data_password != data_confirm_password):
            raise forms.ValidationError("The two passwords field didn't match")
        return data_confirm_password

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'phone', 'first_name', 'last_name']

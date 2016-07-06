from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.template import RequestContext
from account.forms import *

# Create your views here.

def signup(request):
	pass

@require_http_methods(['GET', 'POST'])
def login(request):
	if request.user.is_authenticated():
		return redirect(reverse('dashboard', kwargs={'id': request.user.id}));
	if request.method == 'GET':
		context = { 'f' : LoginForm()};
		return render(request, 'account/login.html', context);
	else:
		f = LoginForm(request.POST);
		if not f.is_valid():
			return render(request, 'account/login.html', {'f' : f});
		else:
			user = f.authenticated_user
			auth_login(request, user)
			return redirect(reverse('dashboard', kwargs = {'id': user.id}));

def forgot_password(request):
	pass

@login_required(login_url = 'login')
@require_http_methods(['GET' , 'POST'])
def reset_password(request , id):
	if(request.method == 'GET'):
		f = ResetPasswordForm(request.user)
		return render(request , 'account/reset_password.html' , {'f' : f , 'success':False})
	elif (request.method == 'POST'):
		f = ResetPasswordForm(request.user , request.POST)
		if not f.is_valid():
			return render(request , 'account/reset_password.html' , {'f' : f , 'success':False})
		request.user.set_password(f.data['new_password'])
		request.user.save()
		return render(request , 'account/reset_password.html' , {'success':True})

@require_GET
@login_required(login_url =  'login')
def logout(request , id):
    auth_logout(request)
    return redirect(reverse('login'));

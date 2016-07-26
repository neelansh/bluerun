from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import calls
from account.models import *
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from trading.forms import *
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Create your views here.
@require_GET
@login_required(login_url = 'login')
def dashboard(request , id):
	context = {}
	user = get_object_or_404(MyUser , id = request.user.id)
	context['user'] = user
	calls_obj = calls.objects.all()

	if(user.cash_intra):
		context['cash_intra'] = None
		try:
			context['cash_intra'] = calls_obj.filter(cash_intra = True).order_by('-created_on')
		except ObjectDoesNotExist:
			print(ObjectDoesNotExist)
	else:
		context['cash_intra'] = "not_subscribed"

	if(user.cash_positional):
		context['cash_positional'] = None
		try:
			context['cash_positional'] = calls_obj.filter(cash_positional = True).order_by('-created_on')
		except ObjectDoesNotExist:
			print(ObjectDoesNotExist)
	else:
		context['cash_positional'] = "not_subscribed"

	if(user.stock_future):
		context['stock_future'] = None
		try:
			context['stock_future'] = calls_obj.filter(stock_future = True).order_by('-created_on')
		except ObjectDoesNotExist:
			print(ObjectDoesNotExist)
	else:
		context['stock_future'] = "not_subscribed"

	if(user.nifty_future):
		context['nifty_future'] = None
		try:
			context['nifty_future'] = calls_obj.filter(nifty_future = True).order_by('-created_on')
		except ObjectDoesNotExist:
			print(ObjectDoesNotExist)
	else:
		context['nifty_future'] = "not_subscribed"

	if(user.option_calls_covered):
		context['option_calls_covered'] = None
		try:
			context['option_calls_covered'] = calls_obj.filter(option_calls_covered = True).order_by('-created_on')
		except ObjectDoesNotExist:
			print(ObjectDoesNotExist)
	else:
		context['option_calls_covered'] = "not_subscribed"

	if(user.option_calls_uncovered):
		context['option_calls_uncovered'] = None
		try:
			context['option_calls_uncovered'] = calls_obj.filter(option_calls_uncovered = True).order_by('-created_on')
		except ObjectDoesNotExist:
			print(ObjectDoesNotExist)
	else:
		context['option_calls_uncovered'] = "not_subscribed"

	if(user.multi_bagger):
		context['multi_bagger'] = None
		try:
			context['multi_bagger'] = calls_obj.filter(multi_bagger = True).order_by('-created_on').order_by('-created_on')
		except ObjectDoesNotExist:
			print(ObjectDoesNotExist)
	else:
		context['multi_bagger'] = "not_subscribed"

	return render(request , 'trading/dashboard.html' , context)


@require_GET
@login_required(login_url = 'login')
def profile(request , id):
    context = {}
    user = get_object_or_404(MyUser , id = request.user.id)
    context['user'] = user
    calls_obj = calls.objects.all()
    return render(request, 'trading/profile.html' , context)

@require_http_methods(['GET' , 'POST'])
@login_required(login_url = 'login')
def editprofile(request , id):
	context ={}
	user = get_object_or_404(MyUser, id = request.user.id)
	# context['user'] = user
	# data = {'first_name':user.first_name, 'last_name':user.last_name, 'phone':user.phone}
	if request.method == 'GET':
		context = { 'f' : EditProfileForm({'first_name': user.first_name,'email' : user.email , 'last_name':user.last_name , 'phone':user.phone})}
		return render(request, 'trading/editprofile.html', context)
	else:
		f = EditProfileForm(request.POST)
		if not f.is_valid():
			return render(request, 'trading/editprofile.html', {'f' : f})
		if user.email != f.data['email']:
			if (MyUser.objects.filter(email = f.data['email']).exists()):
				f.add_error('email','User with this email already exists.')
				return render(request, 'trading/editprofile.html', {'f' : f}) 
			else:
				user.email = f.data['email']
				user.first_name = f.data['first_name']
				user.last_name = f.data['last_name']
				user.phone = f.data['phone']
				user.confirmed_email = False
				user.save()
				try:
					otp = create_otp(user = user, purpose = 'CE')
					email_body_context = { 'u' : user, 'otp' : otp}
					body = loader.render_to_string('trading/confirmemail_email.txt', email_body_context)
					message = EmailMultiAlternatives("Confirm email", body, "bluerunfinancial@gmail.com", [user.email])
					message.send()
					return render(request , 'trading/confirmemail_email_sent.html' , { 'user': user })	
				except ex:
					print(ex)
		else:
			user.first_name = f.data['first_name']
			user.last_name = f.data['last_name']
			user.phone = f.data['phone']
			user.save()
				
		return render(request, 'trading/profile.html', {'user': user})

def confirm_email(request , id , otp):
	user = get_object_or_404(MyUser, id=id)
	otp_object = get_valid_otp_object(user = user, purpose='CE', otp = otp)
	if not otp_object:
		raise Http404()
	user.confirmed_email = True
	user.save()
	otp_object.delete()
	return redirect(reverse('profile' , kwargs={'id': request.user.id}))
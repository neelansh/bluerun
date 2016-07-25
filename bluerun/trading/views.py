from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import calls
from account.models import *
from django.core.exceptions import ObjectDoesNotExist
from trading.forms import *
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Create your views here.
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
	# create context
	# get user id
	# query user models
	# check which facilities are true
	# get calls related to those
	# add them in context
	# if a facility is false
	# 	add a marker
	# render the template 

def profile(request , id):
    context = {}
    user = get_object_or_404(MyUser , id = request.user.id)
    context['user'] = user
    calls_obj = calls.objects.all()
   
    return render(request, 'trading/profile.html' , context)


def editprofile(request , id):
	context ={}
	user = get_object_or_404(MyUser, id = request.user.id)
	context['user'] = user
	if request.method == 'GET':
		context = { 'f' : EditProfileForm()}
		return render(request, 'trading/editprofile.html', context)
	else:
		f = EditProfileForm(request.POST, initial={'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email, 'phone':user.phone})
		if not f.is_valid():
			return render(request, 'trading/editprofile.html', {'f' : f})
		else:
			first_name_def = user.first_name
			last_name_def = user.last_name
			email_def = user.email
			phone_def = user.phone
			user.first_name = request.POST.get('first_name')
			if not user.first_name:
				user.first_name = first_name_def
			user.last_name = request.POST.get('last_name')
			if not user.last_name:
				user.last_name = last_name_def
			user.email = request.POST.get('email')
			if not user.email:
				user.email = email_def
			user.phone = request.POST.get('phone')
			if not user.phone:
				user.phone = phone_def
			user.save(update_fields=['first_name','last_name','phone'])
			if (user.email != email_def):
				otp = create_otp(user = user, purpose = 'AA')
				email_body_context = { 'u' : user, 'otp' : otp}
				body = loader.render_to_string('account/activate_account_email.txt', email_body_context)
				message = EmailMultiAlternatives("Activate Account", body, "bluerunfinancial@gmail.com", [user.email])
				message.send()
				user.save(update_fields=['email'])
				return render(request , 'account/activate_email_sent.html' , { 'user': user })
		return render(request, 'trading/profile.html', {'user': user})


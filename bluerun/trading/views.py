from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import calls
from account.models import MyUser
from django.core.exceptions import ObjectDoesNotExist

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
    data = MyUser.objects.all()
    context['user'] = user
    context['data'] = data
    return render(request, 'trading/profile.html' , context)

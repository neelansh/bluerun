from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.template import RequestContext
from account.forms import *
from .models import *
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import Http404, JsonResponse, HttpResponse

import datetime
import hashlib
from random import randint
# from django.views.decorators.csrf import csrf_protect, csrf_exempt
# from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template
# Create your views here.

@require_http_methods(['GET', 'POST'])
def signup(request):
	if request.user.is_authenticated():
		return redirect(reverse('dashboard', kwargs={'id': request.user.id}))
	if request.method == 'GET':
		context = { 'f' : SignupForm()}
		return render(request, 'account/signup.html', context)
	else:
		f = SignupForm(request.POST)
		if not f.is_valid():
			return render(request, 'account/signup.html', {'f' : f})
		else:
			user = f.save(commit = False)
			user.set_password(f.cleaned_data['password'])
			user.is_active = False
			user.save()
			otp = create_otp(user = user, purpose = 'AA')
			email_body_context = { 'u' : user, 'otp' : otp}
			body = loader.render_to_string('account/activate_account_email.txt', email_body_context)
			message = EmailMultiAlternatives("Activate Account", body, "bluerunfinancial@gmail.com", [user.email])
			message.send()
			return render(request , 'account/activate_email_sent.html' , { 'user': user })

def activate_account(request , id , otp):
	if request.user.is_authenticated():
		return redirect(reverse('dashboard', kwargs={'id': request.user.id}))
	user = get_object_or_404(MyUser, id=id)
	otp_object = get_valid_otp_object(user = user, purpose='AA', otp = otp)
	if not otp_object:
		raise Http404()
	user.is_active = True
	user.confirmed_email = True
	user.save()
	otp_object.delete()
	return render(request , "account/account_active.html" , { 'user' : user })


@require_http_methods(['GET', 'POST'])
def login(request):
	if request.user.is_authenticated():
		return redirect(reverse('dashboard', kwargs={'id': request.user.id}))
	if request.method == 'GET':
		context = { 'f' : LoginForm()}
		return render(request, 'account/login.html', context)
	else:
		f = LoginForm(request.POST)
		if not f.is_valid():
			return render(request, 'account/login.html', {'f' : f})
		else:
			user = f.authenticated_user
			auth_login(request, user)
			return redirect(reverse('dashboard', kwargs = {'id': user.id}))


def forgot_password(request):
	if request.user.is_authenticated():
		return redirect(reverse('dashboard', kwargs={'id': request.user.id}))
	if request.method == 'GET':
		context = { 'f' : ForgotPassword()}
		return render(request, 'account/forgot_password.html', context)
	else:
		f = ForgotPassword(request.POST)
		if not f.is_valid():
			return render(request, 'account/forgot_password.html', {'f' : f})
		else:
			user = MyUser.objects.get(email = f.cleaned_data['email'])
			otp = create_otp(user = user, purpose = 'FP')
			email_body_context = { 'u' : user, 'otp' : otp}
			body = loader.render_to_string('account/forgot_password_email.txt', email_body_context)
			print(user.email)
			message = EmailMultiAlternatives("Reset Password", body, 'bluerunfinancial@gmail.com', [user.email])
			#message.attach_alternative(html_body, 'text/html')
			message.send()
			return render(request, 'account/forgot_email_sent.html', {'u': user})

def set_password(request, id = None, otp = None):
    if request.user.is_authenticated():
    	return redirect(reverse('dashboard', kwargs={'id': request.user.id}))
    user = get_object_or_404(MyUser, id=id)
    otp_object = get_valid_otp_object(user = user, purpose='FP', otp = otp)
    if not otp_object:
        raise Http404()
    if request.method == 'GET':
        f = SetPasswordForm()
    else:
        f = SetPasswordForm(request.POST)
        if f.is_valid():
            user.set_password(f.cleaned_data['new_password'])
            user.save()
            otp_object.delete()
            return render(request, 'account/set_password_success.html', { 'u' : user})
    context = { 'f' : f, 'otp': otp_object.otp, 'uid': user.id}
    return render(request, 'account/set_password.html', context)

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
    return redirect(reverse('login'))


@login_required(login_url = 'login')
@require_http_methods(['GET' , 'POST'])
def subscription(request):
	pass


@login_required(login_url = 'login')
@require_http_methods(['GET' , 'POST'])
def subscription_change(request):
	MERCHANT_KEY = "JBZaLc"
	key ="JBZaLc"
	SALT = "GQs7yium"
	PAYU_BASE_URL = "https://test.payu.in/_payment"
	action = ''
	posted = { "surl":reverse('subscription_success'),
	"furl":reverse('subscription_failure'),
	"firstname": request.user.first_name,
	"email": request.user.email,
	"phone": request.user.phone, }
	for i in request.POST:
		posted[i] = request.POST[i]
	hash_object = hashlib.sha256(b'randint(0,20)')
	txnid = hash_object.hexdigest()[0:20]
	hashh = ''
	posted['txnid'] = txnid
	hashSequence = "key|txnid|amount|productinfo|firstname|email||||||||||"
	posted['key'] = key
	hash_string = ''
	hashVarsSeq = hashSequence.split('|')
	for i in hashVarsSeq:
		try:
			hash_string += str(posted[i])
		except Exception:
			hash_string += ''
		hash_string += '|'
	hash_string += SALT
	hash_string = hash_string.encode('utf-8')
	hashh = hashlib.sha512(hash_string).hexdigest().lower()
	action = PAYU_BASE_URL
	if(posted.get("key")!=None and posted.get("txnid")!=None and posted.get("productinfo")!=None and posted.get("firstname")!=None and posted.get("email")!=None):
		return render_to_response('account/subscription.html',RequestContext(request,{"posted":posted,"hashh":hashh,"MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,"action":"https://test.payu.in/_payment" }))
	else:
		return render_to_response('account/subscription.html',RequestContext(request,{"posted":posted,"hashh":hashh,"MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,"action":"." }))

@login_required(login_url = 'login')
@require_http_methods(['GET' , 'POST'])
def subscription_success(request):
	c = {}
	c.update(csrf(request))
	status=request.POST["status"]
	firstname=request.POST["firstname"]
	amount=request.POST["amount"]
	txnid=request.POST["txnid"]
	posted_hash=request.POST["hash"]
	key=request.POST["key"]
	productinfo=request.POST["productinfo"]
	email=request.POST["email"]
	salt="GQs7yium"
	try:
		additionalCharges=request.POST["additionalCharges"]
		retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	except Exception:
		retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
	if(hashh !=posted_hash):
		print("Invalid Transaction. Please try again")
	else:
		print ("Thank You. Your order status is ", status)
		print ("Your Transaction ID for this transaction is ",txnid)
		print ("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")
	return render_to_response('account/subscription_success.html',RequestContext(request,{"txnid":txnid,"status":status,"amount":amount}))


@login_required(login_url = 'login')
@require_http_methods(['GET' , 'POST'])
def subscription_failure(request):
	c = {}
	c.update(csrf(request))
	status=request.POST["status"]
	firstname=request.POST["firstname"]
	amount=request.POST["amount"]
	txnid=request.POST["txnid"]
	posted_hash=request.POST["hash"]
	key=request.POST["key"]
	productinfo=request.POST["productinfo"]
	email=request.POST["email"]
	salt="GQs7yium"
	try:
		additionalCharges=request.POST["additionalCharges"]
		retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	except Exception:
		retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
	if(hashh !=posted_hash):
		print ("Invalid Transaction. Please try again")
	else:
		print ("Thank You. Your order status is ", status)
		print ("Your Transaction ID for this transaction is ",txnid)
		print ("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")
	return render_to_response("account/subscription_failure.html",RequestContext(request,c))
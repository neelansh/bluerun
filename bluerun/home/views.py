from django.shortcuts import render
from .models import Contact
from .forms import ContactForm
from django import forms
from django.contrib import messages 
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from trading.models import calls

# Create your views here.

def index(request):
	context = {}
	context['call_obj'] = calls.objects.filter(achived = True).order_by('-created_on')[:5]
	return render(request , 'home/index.html', context)

def aboutus(request):
	return render(request , 'home/about-us.html')

def services(request):
	return render(request , 'home/services.html')

def marketoutlook(request):
	return render(request , 'home/marketoutlook.html')

def pricing(request):
	return render(request , 'home/pricing.html')

@require_http_methods(['POST' , 'GET'])
def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            subject = request.POST.get('subject' , '')
            message = request.POST.get('message', '')
            forminstance = Contact(name = name,email = email,contact = contact,subject = subject,message = message)
            forminstance.save()
            messages.success(request, 'Submitted successfully!')                
    else:
        form = ContactForm()
    
    return render(request , 'home/contact-us.html')

def careers(request):
	return render(request , 'home/careers.html')

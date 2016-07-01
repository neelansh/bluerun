from django.shortcuts import render

# Create your views here.

def index(request):
	return render(request , 'home/index.html')

def aboutus(request):
	return render(request , 'home/about-us.html')

def services(request):
	return render(request , 'home/services.html')

def portfolio(request):
	return render(request , 'home/portfolio.html')

def pricing(request):
	return render(request , 'home/pricing.html')

def contactus(request):
	return render(request , 'home/contact-us.html')

def careers(request):
	return render(request , 'home/careers.html')
from django.contrib import admin
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import calls
from account.models import MyUser

# Register your models here.

class CallsAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		users = MyUser.objects.filter(cash_intra = True)
		for user in users:
			email_field = user.email
			if(obj.cash_intra):	
				subject, from_email = 'Subscription Update', 'bluerunfinancial@gmail.com'
				body = loader.render_to_string('trading/text.txt')
				msg = EmailMultiAlternatives(subject, body, from_email, [email_field])
				msg.send()	
		obj.save()
	
admin.site.register(calls, CallsAdmin)



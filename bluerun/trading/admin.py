from django.contrib import admin
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import calls
from account.models import MyUser

# Register your models here.

class CallsAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		if(obj.id is None):
			query = "SELECT id,email,first_name FROM account_myuser WHERE"
			if(obj.cash_intra):
				query = query + " cash_intra = b'1' OR"
			if(obj.cash_positional):
				query = query + " cash_positional = b'1' OR"
			if(obj.stock_future):
				query = query + " stock_future = b'1' OR"
			if(obj.nifty_future):
				query = query + " nifty_future = b'1' OR"
			if(obj.option_calls_covered):
				query = query + " option_calls_covered = b'1' OR"
			if(obj.option_calls_uncovered):
				query = query + " option_calls_uncovered = b'1' OR"
			if(obj.multi_bagger):
				query = query + " multi_bagger = b'1' OR"
			query = query[:-2]
			query =query + ";"
			for q in MyUser.objects.raw(query):
				email_field = q.email
				subject, from_email = 'Subscription Update', 'bluerunfinancial@gmail.com'
				body = loader.render_to_string('trading/text.txt')
				msg = EmailMultiAlternatives(subject, body, from_email, [email_field])
				msg.send()

		obj.save()
				
	
admin.site.register(calls, CallsAdmin)
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
	phone = models.CharField(max_length = 10, null = True)
	cash_intra = models.BooleanField(default = False)
	cash_positional = models.BooleanField(default = False)
	stock_future = models.BooleanField(default = False)
	nifty_future = models.BooleanField(default = False)
	option_calls_covered = models.BooleanField(default = False)
	option_calls_uncovered = models.BooleanField(default = False)
	multi_beggar = models.BooleanField(default = False)
	subscription_startdate = models.DateTimeField(null = True)
	subscription_enddate = models.DateTimeField(null = True)
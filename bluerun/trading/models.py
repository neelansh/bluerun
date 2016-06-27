from django.db import models

# Create your models here.
class calls(models.Model):
	created_on = models.DateTimeField(auto_now_add = True)
	stock_name = models.CharField(max_length = 100)
	entry_price = models.IntegerField()
	target = models.IntegerField()
	stop_loss = models.IntegerField()
	time_frame = models.CharField(max_length = 100)
	comment = models.CharField(max_length = 500 , blank = True , null = True)
	cash_intra = models.BooleanField(default = False)
	cash_positional = models.BooleanField(default = False)
	stock_future = models.BooleanField(default = False)
	nifty_future = models.BooleanField(default = False)
	option_calls_covered = models.BooleanField(default = False)
	option_calls_uncovered = models.BooleanField(default = False)
	multi_beggar = models.BooleanField(default = False)

	def __str__(self):
		return self.stock_name


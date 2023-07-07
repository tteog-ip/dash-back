from django.db import models

# Create your models here.
class DailyUsage(models.Model):
    date = models.CharField(max_length=10)
    price = models.IntegerField()
    class Meta:
        db_table = 'daily_usage'

class MonthlyUsage(models.Model):
    month = models.CharField(max_length=10)
    price = models.IntegerField()
    class Meta:
        db_table = 'monthly_usage'
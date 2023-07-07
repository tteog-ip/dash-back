from django.db import models

# Create your models here.
class ResourcePrice(models.Model):
    date = models.CharField(max_length=10)
    ec2Price = models.FloatField()
    ebsPrice = models.FloatField()
    eksPrice = models.FloatField()
    esPrice = models.FloatField()
    rdsPrice = models.FloatField()
    class Meta:
        db_table = 'resource_price'
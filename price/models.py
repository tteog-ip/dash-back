from django.db import models

class ResourceType(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'resource_type'

class Price(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=300)
    type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    class Meta:
        db_table = 'price'
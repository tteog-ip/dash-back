from django.shortcuts import render
from django.views import View
import boto3

# Create your views here.
class PriceView(View):
    def get(self):
        try:
            pricing_client = boto3.client('pricing', region_name='us-east-1')

            return 0
        except:
            return 0



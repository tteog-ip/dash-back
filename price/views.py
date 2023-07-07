from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import responses, Response
from django.http import Http404

from .serializers import *
from .models import *
from scheduler.models import ResourcePrice

# Create your views here.

class DailyUsageList(APIView):
    def get(self, request):
        # show daily data from rds
        today = DailyUsage.objects.all()
        serializers = DailyUsageSerializer(today, many=True)
        return Response(serializers.data)

class MonthlyUsageList(APIView):
    def get(self, request):
        # show daily data from rds
        month = MonthlyUsage.objects.all()
        serializers = MonthlyUsageSerializer(month, many=True)
        return Response(serializers.data)

class ResourceUsageList(APIView):
    def get(self, request):
        # show daily data from rds
        resource = ResourcePrice.objects.all()
        serializers = ResourcePriceSerializer(resource, many=True)
        return Response(serializers.data)
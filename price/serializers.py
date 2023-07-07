# serialize: Queryset을 JSON으로 매핑 (들어오는 데이터는 JSON)
# serializer: DRF가 제공하는 클래스
# -> DB 인스턴스를 JSON 객체로 데이터로 바꿔준다
# 장고의 FORM과 유사

from rest_framework import serializers
from .models import *
from scheduler.models import ResourcePrice

class DailyUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyUsage
        fields = ('date', 'price')

class MonthlyUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyUsage
        fields = ('month', 'price')

class ResourcePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourcePrice
        fields = ('date', 'ec2Price', 'ebsPrice', 'eksPrice', 'esPrice', 'rdsPrice')

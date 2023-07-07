from django.shortcuts import render
from django.conf import settings
import datetime
from .models import *
from .calculate import *
from price.models import *

# Create your views here.
def save_data_to_db():
    # 일일 리소스별 비용 디비에 저장
    resource = ResourcePrice()
    resource.date = datetime.today().strftime("%Y%m%d")
    resource.ec2Price = CostEC2()
    resource.ebsPrice = CostEBS()
    resource.eksPrice = CostEKS()
    resource.esPrice = CostES()
    resource.rdsPrice = CostRDS()
    resource.save()

def daily_usage():
    # 일일 전체 비용 디비에 저장
    daily = daily_usage()
    daily.date = datetime.today().strftime("%Y%m%d")
    daily.price = day_of_usage
    daily.save()

def monthly_usage():
    # 한 달 전체 비용 디비에 저장
    month = monthly_usage()
    month.month = datetime.today().strftime("%Y%m")

    # 시작 날짜
    first_day = datetime(datetime.today().year, datetime.today().month, 1)
    first_day_str = first_day.strftime("%Y%m%d")
    # 이번 달 일일 비용 불러오기
    daily = daily_usage().objects.filter(date__gte=first_day_str, date__lt=datetime.today().strftime("%Y%m%d"))
    total_price = sum(d.price for d in daily)
    # 더해서 저장
    month.price = total_price
    month.save()
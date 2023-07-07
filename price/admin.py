from django.contrib import admin
from .models import *

# Register your models here.

# 장고에서 제공해주는 관리자 페이지로 데이터베이스 조작 가능
admin.site.register(DailyUsage)
admin.site.register(MonthlyUsage)

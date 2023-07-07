from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('today/', DailyUsageList.as_view()),
    path('month/', MonthlyUsageList.as_view()),
    path('resource/', ResourceUsageList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
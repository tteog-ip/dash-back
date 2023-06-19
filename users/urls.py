from django.urls import path

from .views import SigninView

urlpatterns = [
    path('/login', SigninView.as_view()),
]
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegiserAPIView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
]

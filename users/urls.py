from django.urls import path
from . import views

urlpatterns = [
    path("sign-up", views.SignUpView.as_view()),
    path("logout", views.LogOutView.as_view()),
]

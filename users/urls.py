from django.urls import path
from . import views

urlpatterns = [
    path("sign-up", views.SignUpView.as_view()),
    path("logout", views.LogOutView.as_view()),
    path("login", views.LogInView.as_view()),
    path("me", views.PrivateUserView.as_view()),
    path("change-password", views.ChangePasswordView.as_view()),
]

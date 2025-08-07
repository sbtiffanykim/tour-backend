from django.urls import path
from . import views

urlpatterns = [
    path("create", views.CreateWishlistView.as_view()),
    path("<int:pk>", views.WishlistDetailView.as_view()),
]

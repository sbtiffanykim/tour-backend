from django.urls import path
from . import views

urlpatterns = [
    path("create", views.CreateWishlistView.as_view()),
    path("<int:pk>", views.WishlistDetailView.as_view()),
    path("<int:pk>/add/<int:accommodation_pk>", views.AddAccommodationToWishlistView.as_view()),
    path("<int:pk>/remove/<int:accommodation_pk>", views.RemoveAccommodationFromWishlistView.as_view()),
]

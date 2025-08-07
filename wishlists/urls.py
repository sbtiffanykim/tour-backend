from django.urls import path
from . import views

urlpatterns = [path("<int:pk>", views.WishlistDetailView.as_view())]

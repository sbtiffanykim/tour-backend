from django.urls import path
from . import views

urlpatterns = [path("", views.AccommodationListView.as_view())]

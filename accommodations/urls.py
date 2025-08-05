from django.urls import path
from . import views

urlpatterns = [
    path("", views.AccommodationListView.as_view()),
    path("<int:pk>", views.AccommodationDetailView.as_view()),
    path("<int:pk>/room-packages", views.AllPackageCombinationsView.as_view()),
    path("<int:pk>/available-room-packages", views.AvailableRoomPackagesView.as_view()),
]

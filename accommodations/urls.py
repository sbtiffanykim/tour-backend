from django.urls import path
from . import views
from packages.views import RoomPackageListView, AvailableRoomPackagesView

urlpatterns = [
    path("", views.AccommodationCollectionView.as_view()),  # GET, POST
    path("<int:pk>", views.AccommodationDetailView.as_view()),
    path("<int:pk>/room-packages", RoomPackageListView.as_view()),
    path("<int:pk>/available-room-packages", AvailableRoomPackagesView.as_view()),
    path("amenities", views.AmenityCollectionView.as_view()),  # GET, POST
    path("cities", views.CityCollectionView.as_view()),  # GET, POST
]

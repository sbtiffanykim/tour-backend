from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/accommodations/", include("accommodations.urls")),
    path("api/v1/wishlists/", include("wishlists.urls")),
    path("api/v1/bookings/", include("bookings.urls")),
]

from django.contrib import admin
from .models import Accommodation, Amenity, City


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "city")
    list_filter = ("region", "type")
    search_fields = ("name", "city")


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass

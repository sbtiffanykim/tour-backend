from django.contrib import admin
from .models import Accommodation, Amenity


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ("name", "region")
    list_filter = ("region",)
    search_fields = ("name",)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass

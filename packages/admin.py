from django.contrib import admin
from .models import Package, PackageDailyAvailability


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "price"]
    list_filter = ["room_type__accommodation__name"]
    search_fields = ["name", "room_type__name", "room_type__accommodation__name"]


@admin.register(PackageDailyAvailability)
class PackageDailyAvailabilityAdmin(admin.ModelAdmin):
    list_display = ["__str__", "price"]
    search_fields = ["package"]

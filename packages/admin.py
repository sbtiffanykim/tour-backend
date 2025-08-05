from django.contrib import admin
from .models import Package, PackagePrice


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "price"]
    list_filter = ["room_type__accommodation__name"]
    search_fields = ["name", "room_type__name", "room_type__accommodation__name"]


@admin.register(PackagePrice)
class PackagePriceAdmin(admin.ModelAdmin):
    pass

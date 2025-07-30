from django.contrib import admin
from .models import RoomType, BedConfiguration


class BedConfigurationInline(admin.TabularInline):
    model = BedConfiguration
    extra = 1


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ["accommodation", "name", "base_occupancy", "max_occupancy"]
    fieldsets = [
        (("Info"), {"fields": ["accommodation", "name", "base_occupancy", "max_occupancy", "description"]}),
        (("Number of rooms"), {"fields": ["num_living_room", "num_bedrooms", "num_bathrooms"]}),
    ]
    list_filter = ["accommodation__name"]
    search_fields = ["name", "accommodation__name"]
    inlines = [BedConfigurationInline]


@admin.register(BedConfiguration)
class BedConfigureAdmin(admin.ModelAdmin):
    list_display = ["room_type", "bed_type", "count"]
    list_filter = ["room_type__accommodation__name"]
    search_fields = ["room_type__name", "room_type__accommodation__name"]

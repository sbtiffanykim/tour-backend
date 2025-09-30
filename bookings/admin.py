from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["user_or_guest", "package", "check_in", "check_out", "status"]
    list_filter = ["status"]

    def user_or_guest(self, obj):
        if obj.guest_user:
            return obj.guest_user.first_name
        return obj.user.username

    user_or_guest.short_description = "User"

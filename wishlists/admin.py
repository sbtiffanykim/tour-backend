from django.contrib import admin
from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["__str__", "user", "num_of_accommodations"]
    list_filter = ["user", "accommodations"]
    search_fields = ["accommodations__name", "user__username"]

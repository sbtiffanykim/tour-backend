from django.db import models
from users.models import User, GuestInfo
from packages.models import Package, PackageDailyAvailability


class BookingStatusChoices(models.TextChoices):
    """Booking status visible to customers"""

    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    DENIDED = "denied", "Denied"


class Booking(models.Model):
    """Main Booking model for users. Staff-only payment/refund info is separated into BookingAdminInfo"""

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    # Link to a registered user (nullable if guest)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="bookings", blank=True, null=True)
    # Link to a guest info (for non-registered customers)
    guest_user = models.ForeignKey(GuestInfo, on_delete=models.SET_NULL, related_name="bookings", blank=True, null=True)
    # Link to a package (e.g. room only, breakfast included)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="bookings")
    # Daily availabilities connected through BookingLineItem
    daily_availabilities = models.ManyToManyField(PackageDailyAvailability, through="BookingLineItem")
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    guests = models.PositiveSmallIntegerField()
    # Status visible to customers
    status = models.CharField(max_length=20, choices=BookingStatusChoices, default=BookingStatusChoices.PENDING)

    def __str__(self):
        return f"Booking #{self.id}"


class BookingLineItem(models.Model):
    """Middle table connecting Booking and PackageDailyAvailability. Stores daily prices for each reserved date."""

    booking = models.ForeignKey("Booking", on_delete=models.CASCADE, related_name="line_items")
    daily_availability = models.ForeignKey(PackageDailyAvailability, on_delete=models.CASCADE)

    # Final applied prices for the date (copied or overridden)
    retail_price = models.PositiveIntegerField()
    cost_price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.booking} - {self.daily_availability.date}"


class BookingAdminInfo(models.Model):
    """Staff-only extended information for bookings."""

    booking = models.OneToOneField("Booking", on_delete=models.CASCADE, related_name="admin_info")
    staff_note = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Admin info for Booking #{self.booking.id}"

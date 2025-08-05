from django.db import models
from room_types.models import RoomType


class Package(models.Model):
    """Model Definition for package"""

    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="packages")
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField(help_text="default price in KRW")
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_type} - {self.name}"


class AvailabilityStatus(models.TextChoices):
    OPEN = "open", "Open"
    CLOSED = "close", "Unavailable"


class PackageDailyAvailability(models.Model):
    """Daily availability and price for a package"""

    package = models.ForeignKey("packages.Package", on_delete=models.CASCADE, related_name="daily_prices")
    date = models.DateField()
    price = models.PositiveIntegerField(help_text="daily price in KRW")
    status = models.CharField(
        max_length=15,
        choices=AvailabilityStatus,
        default=AvailabilityStatus.OPEN,
        help_text="Availability status of the package on a specific date",
    )

    class Meta:
        unique_together = ("package", "date")
        verbose_name = "Package Daily Availability"
        verbose_name_plural = "Package Daily Availabilities"

    def __str__(self):
        return f"{self.package.room_type}-{self.package.name} | {self.date} : {self.status}"

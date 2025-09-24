from django.db import models
from room_types.models import RoomType


class Package(models.Model):
    """Model Definition for package"""

    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="packages")
    name = models.CharField(max_length=50)
    base_price = models.PositiveIntegerField(help_text="Default base price in KRW")  # staff only
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_type} - {self.name}"


class AvailabilityStatus(models.TextChoices):
    OPEN = "open", "Open"
    CLOSED = "close", "Unavailable"


class Weekday(models.IntegerChoices):
    SUNDAY = 0, "Sunday"
    MONDAY = 1, "Monday"
    TUESDAY = 2, "Tuesday"
    WEDNESDAY = 3, "Wednesday"
    THURSDAY = 4, "Thursday"
    FRIDAY = 5, "Friday"
    SATURDAY = 6, "Saturday"


class PackageWeekdayBasePrice(models.Model):
    package = models.ForeignKey("packages.Package", on_delete=models.CASCADE, related_name="weekday_base_prices")
    weekday = models.IntegerField(choices=Weekday.choices)
    retail_price = models.PositiveIntegerField(help_text="Default selling price in KRW")
    cost_price = models.PositiveIntegerField(help_text="Internal coast price in KRW")

    class Meta:
        unique_together = ("package", "weekday")
        verbose_name = "Package Weekday Base Price"
        verbose_name_plural = "Package Weekday Base Prices"

    def __str__(self):
        return f"{self.package.name} - {self.get_weekday_display()}: {self.retail_price} / {self.cost_price}"


class PackageDailyAvailability(models.Model):
    """Daily availability and price for a package"""

    package = models.ForeignKey("packages.Package", on_delete=models.CASCADE, related_name="daily_prices")
    date = models.DateField()
    retail_price = models.PositiveIntegerField(help_text="Override retail price (optional)")
    cost_price = models.PositiveIntegerField(help_text="Override cost price (optional)")  # staff only
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

    def get_effective_prices(self):
        """Return daily retail and cost price, falling back to weekday base price"""
        if self.retail_price and self.cost_price:
            return self.retail_price, self.cost_price

        weekday = self.date.weekday()
        try:
            base = self.package.weekday_base_prices.get(weekday=weekday)
            return base.retail_price, base.cost_price
        except PackageWeekdayBasePrice.DoesNotExist:
            return None, None

    def __str__(self):
        return f"{self.package.room_type}-{self.package.name} | {self.date} : {self.status}"

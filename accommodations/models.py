from django.db import models


class RegionChioce(models.TextChoices):
    SEOUL = "seoul", "Seoul"
    GYEONGGI = "gyeonggi", "Gyeonggi"
    GANGWON = "gangwon", "Gangwon"
    CHUNGCHEONG = "chungcheong", "Chungcheong"
    GYEONGSANG = "gyeongsang", "Gyeongsang"
    JEOLLA = "jeolla", "Jeolla"
    JEJU = "jeju", "Jeju"


class AccommodationType(models.TextChoices):
    HOTEL = "hotel", "Hotel"
    RESORT = "resort", "Resort"


class Accommodation(models.Model):
    """Model Definition for accomodations"""

    name = models.CharField(max_length=50)
    location = models.CharField(max_length=150)
    region = models.CharField(max_length=20, choices=RegionChioce)
    city = models.ForeignKey("accommodations.City", on_delete=models.SET_NULL, null=True, related_name="accommodations")
    type = models.CharField(max_length=10, choices=AccommodationType, default=AccommodationType.RESORT)
    x_coordinate = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    y_coordinate = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    homepage = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    cancellation_policy = models.TextField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    amenities = models.ManyToManyField("accommodations.Amenity", related_name="accomodations", null=True, blank=True)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    """Model Definition for property amenities"""

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    icon = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name


class City(models.Model):
    """Model Definition for cities"""

    name = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name

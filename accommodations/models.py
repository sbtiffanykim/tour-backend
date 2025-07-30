from django.db import models


class Accommodation(models.Model):
    """Model Definition for accomodations"""

    name = models.CharField(max_length=50)
    location = models.CharField(max_length=150)
    x_coordinate = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    y_coordinate = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    homepage = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    cancellation_policy = models.TextField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    amenities = models.ManyToManyField("rooms.Amenity", related_name="accomodations")


class Amenity(models.Model):
    """Model Definition for property amenities"""

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    icon = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name

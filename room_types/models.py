from django.db import models
from accommodations.models import Accommodation


class BedType(models.TextChoices):
    SINGLE = "single", "Single"
    SUPERSINGLE = "superSingle", "SuperSingle"
    TWIN = "Twin", "Twin"
    QUEEN = "Queen", "Queen"
    KING = "king", "King"
    SUPERKING = "SuperKing", "SuperKing"
    BUNK = "bunk", "BUNK"
    KOREAN = "korean", "Korean Bedding"


class BedConfiguration(models.Model):
    bed_type = models.CharField(max_length=20, choices=BedType.choices)
    count = models.PositiveSmallIntegerField()


class RoomType(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name="room_type")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    base_occupancy = models.PositiveSmallIntegerField(help_text="기준 인원")
    max_occupancy = models.PositiveSmallIntegerField(help_text="최대 인원")
    area = models.DecimalField(max_digits=4, decimal_places=2, help_text="객실 면적", null=True, blank=True)
    num_living_room = models.PositiveSmallIntegerField(default=1, help_text="거실 수")
    num_bedrooms = models.PositiveSmallIntegerField(default=0, help_text="침실 수")
    num_bathroos = models.PositiveSmallIntegerField(default=0, help_text="화장실 수")
    beds = models.ManyToManyField(BedConfiguration, blank=True)

    def __str__(self):
        return self.name

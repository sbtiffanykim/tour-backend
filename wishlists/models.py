from django.db import models
from users.models import User
from accommodations.models import Accommodation


class Wishlist(models.Model):
    name = models.CharField(max_length=40)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlists")
    accommodations = models.ManyToManyField(Accommodation, related_name="wishlists", blank=True)

    def num_of_accommodations(self):
        return self.accommodations.count()

    def __str__(self):
        return self.name

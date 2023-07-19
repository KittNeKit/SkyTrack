from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_bit_city = models.CharField(max_length=255)


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="source"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="destination"
    )
    distance = models.IntegerField()

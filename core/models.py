from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ReferencePhoto(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    image = models.ImageField(upload_to="photos/")

    x_coord = models.FloatField()
    y_coord = models.FloatField()
    z_coord = models.FloatField(default=0)

    floor = models.IntegerField(default=1)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Фото {self.id} ({self.location})"
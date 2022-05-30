from django.db import models

class Image(models.Model):
    hash = models.BinaryField(max_length=20, null=True, blank=True)
    url = models.CharField(max_length=250, default="")
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=10, default="")

    class Meta:
        ordering = ['id']
from django.db import models

from auth_app.models import CustomUser
from const.const import Genre


class Track(models.Model):
    title = models.CharField(max_length=250)
    singer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="tracks"
    )
    genre = models.CharField(choices=Genre.choices())

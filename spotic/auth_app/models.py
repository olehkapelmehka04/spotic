from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser

from genres import GenreChoices


class CustomUser(AbstractUser):

    role = models.CharField(
        max_length=20,
        choices=[
            ("listener", "Слушатель"),
            ("singer", "Исполнитель"),
            ("admin", "Администратор"),
        ],
        default="listener",
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Активный"),
            ("freze", "Замороженный"),
            ("block", "Заблокированный"),
        ],
        default="active",
    )

    genres = models.CharField(max_length=45, choices=GenreChoices, null=True, blank=True)
from django.db import models
from django.contrib.auth.models import AbstractUser


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
            ("frozen", "Замороженный"),
            ("block", "Заблокированный"),
        ],
        default="active",
    )

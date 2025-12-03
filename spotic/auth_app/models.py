from django.contrib.auth.models import AbstractUser
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50)


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

    genres = models.ManyToManyField(Genre, blank=True, related_name='users')

    def add_genre(self, genre_name):
        try:
            genre = Genre.objects.get(name=genre_name)
            self.genres.add(genre)
            return True
        except Genre.DoesNotExist:
            return False

    def remove_genre(self, genre_name):
        try:
            genre = Genre.objects.get(name=genre_name)
            self.genres.remove(genre)
            return True
        except Genre.DoesNotExist:
            return False

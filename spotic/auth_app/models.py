from django.db import models



class MusicProfile(models.Model):
    user = models.OneToOne(CustomUser, on_delete=models.CASCADE, related_name='music_profile')

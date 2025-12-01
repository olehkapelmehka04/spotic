from decimal import Decimal

from django.db import models





class MusicProfile(models.Model):
    user = models.OneToOne(CustomUser, on_delete=models.CASCADE, related_name='music_profile')
    rock_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    pop_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    jazz_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    blues_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    hip_hop_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    rap_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    classical_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    electronic_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    house_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    techno_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    metal_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    punk_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    country_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    reggae_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    folk_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    rnb_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    soul_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    disco_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    trap_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    drum_and_bass_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    indie_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    lofi_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    ambient_points = models.DecimalField(decimal_places=1, default=Decimal(0))
    soundtrack_points = models.DecimalField(decimal_places=1, default=Decimal(0))
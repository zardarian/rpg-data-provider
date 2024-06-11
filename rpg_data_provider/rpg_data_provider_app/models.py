from django.db import models

# Create your models here.
class RpgEvents(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    updated_at = models.DateTimeField(blank=True, null=True)
    hotel_id = models.BigIntegerField(blank=True, null=True)
    room_id = models.BigIntegerField(blank=True, null=True)
    rpg_status = models.BigIntegerField(blank=True, null=True)
    night_of_stay = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'rpg_events'

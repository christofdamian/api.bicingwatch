from django.db import models

class Station(models.Model):
    class Meta:
        db_table = 'station'
        unique_together = ('x','y')
    
    name = models.CharField(max_length=200)
    x = models.FloatField()
    y = models.FloatField()
    created = models.DateTimeField(auto_now_add = True)
    
class Ping(models.Model):
    class Meta:
        db_table = 'ping'
    
    STATUS_CHOICES = (
        ('G', 'Green'),
        ('R', 'Red'),
    )
    
    station = models.ForeignKey(Station)
    free = models.SmallIntegerField()
    bikes = models.SmallIntegerField()
    status = models.CharField(max_length=1, choices = STATUS_CHOICES)
    timestamp = models.DateTimeField()

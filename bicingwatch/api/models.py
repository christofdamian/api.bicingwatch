from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=200)
    coordinates = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add = True)
    
class Ping(models.Model):
    STATUS_CHOICES = (
        ('G', 'Green'),
        ('R', 'Red'),
    )
    
    station = models.ForeignKey(Station)
    free = models.SmallIntegerField()
    bikes = models.SmallIntegerField()
    status = models.CharField(max_length=1, choices = STATUS_CHOICES)
    timestamp = models.DateTimeField()

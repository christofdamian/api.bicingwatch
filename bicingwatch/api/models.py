from django.db import models

class Station(models.Model): 
    name = models.CharField(max_length=200)
    number = models.PositiveIntegerField(null = True)
    x = models.FloatField()
    y = models.FloatField()
    created = models.DateTimeField()
    
    class Meta:
        db_table = 'station'
        unique_together = ('x','y')
        
    class Admin:
        list_display = ('name', 'created')
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
    
class Ping(models.Model):
    STATUS_GREEN = 1
    STATUS_RED = 2
    STATUS_CHOICES = (
        (STATUS_GREEN, 'Green'),
        (STATUS_RED, 'Red'),
    )
    
    station = models.ForeignKey(Station)
    free = models.PositiveSmallIntegerField()
    bikes = models.PositiveSmallIntegerField()
    status = models.PositiveSmallIntegerField(
        max_length=1, 
        choices = STATUS_CHOICES)
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'ping'
        
    class Admin:
        list_display = ('station', 'free', 'bikes', 'status', 'timestamp')
        ordering = ('station','timestamp')
    
    def __unicode__(self):
        return u"%s %s" % (self.station, self.timestamp)
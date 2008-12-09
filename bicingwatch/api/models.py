from django.db import models

class Station(models.Model): 
    name = models.CharField(max_length=200)
    number = models.PositiveIntegerField(null = True)
    x = models.FloatField()
    y = models.FloatField()
    created = models.DateTimeField()
    address = models.CharField(max_length=200)
    
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
    free = models.SmallIntegerField()
    bikes = models.SmallIntegerField()
    status = models.SmallIntegerField(
        max_length=1, 
        choices = STATUS_CHOICES)
    timestamp = models.DateTimeField()

    @staticmethod
    def __customquery(query , *params):
        """custom sql query"""
        
        from itertools import *
        from django.db import connection
        
        cursor = connection.cursor()
        cursor.execute(query , params)
        col_names = [desc[0] for desc in cursor.description]
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            row_dict = dict(izip(col_names, row))
            yield row_dict
        return

    @staticmethod
    def avg_by_hour(station_id,days = [0,1,2,3,4,5,6]):
        "averages by hour"
        
        return Ping.__customquery('''
            select 
                round(avg(free)) as free,
                round(avg(bikes)) as bikes,
                hour(timestamp) as hour 
            from 
                ping 
            where 
                station_id=%s 
                and weekday(timestamp) in %s
            group by hour''', station_id, days)

    @staticmethod
    def last_24_hours(station_id):
        "last 24 hours"
        
        return Ping.__customquery('''
            select 
                avg(free) as free,
                avg(bikes) as bikes,
                hour(timestamp)  as hour 
            from 
                ping 
            where 
                station_id=%s 
                and now() <= (timestamp + interval 1 day) 
            group by hour
            order by timestamp
        ''', station_id)

    @staticmethod
    def today(station_id):
        "todays free + bikes by time"
        
        return Ping.__customquery('''
            select 
                avg(free) as free,
                avg(bikes) as bikes,
                hour(timestamp)+floor(minute(timestamp)/30)/2 as time 
            from 
                ping 
            where 
                station_id=%s 
                and timestamp >= date(now()) 
            group by time
            order by timestamp
        ''', station_id)
        
    @staticmethod 
    def max(station_id):
        "max bikes and free for station"    

        # TODO: the following is ugly
        for row in Ping.__customquery('''
            select 
                max(free) as free,
                max(bikes) as bikes,
                max(free+bikes) as max
            from 
                ping 
            where 
                station_id=%s 
        ''', station_id):
            return row
                
    class Meta:
        db_table = 'ping'
        
    class Admin:
        list_display = ('station', 'free', 'bikes', 'status', 'timestamp')
        ordering = ('station','timestamp')
    
    def __unicode__(self):
        return u"%s %s" % (self.station, self.timestamp)
from django.db import models

# Create your models here.
class Tracks(models.Model):
    track_name = models.CharField(max_length=255)
    artists = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    popularity = models.IntegerField()
    duration_ms = models.IntegerField()
    explicit = models.BooleanField()
    danceability = models.DecimalField(max_digits=5, decimal_places=3) 
    energy = models.DecimalField(max_digits=5, decimal_places=3)        
    key = models.IntegerField()
    loudness = models.DecimalField(max_digits=6, decimal_places=3)      
    mode = models.IntegerField()
    speechiness = models.DecimalField(max_digits=5, decimal_places=3)   
    acousticness = models.DecimalField(max_digits=5, decimal_places=3)  
    instrumentalness = models.DecimalField(max_digits=8, decimal_places=5) 
    liveness = models.DecimalField(max_digits=5, decimal_places=3)      
    valence = models.DecimalField(max_digits=5, decimal_places=3)       
    tempo = models.DecimalField(max_digits=6, decimal_places=3)        
    time_signature = models.IntegerField()
    

    def __str__(self):
        return self.name
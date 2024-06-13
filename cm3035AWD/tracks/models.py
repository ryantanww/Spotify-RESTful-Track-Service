from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Album(models.Model):
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, related_name='albums', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Track(models.Model):
    track_name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, related_name='tracks', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, related_name='tracks', on_delete=models.CASCADE)
    popularity = models.IntegerField()
    duration_ms = models.IntegerField()
    explicit = models.BooleanField()
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.IntegerField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    time_signature = models.IntegerField()
    

    def __str__(self):
        return self.name
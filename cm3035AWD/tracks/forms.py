from django import forms
from django.forms import ModelForm
from .models import *

class TrackForm(ModelForm):

    def clean(self):
        cleaned_data = super(TrackForm, self).clean()
        popularity = cleaned_data.get("popularity")
        danceability = cleaned_data.get("danceability")
        energy = cleaned_data.get("energy")
        loudness = cleaned_data.get("loudness")
        speechiness = cleaned_data.get("speechiness")
        acousticness = cleaned_data.get("acousticness")
        instrumentalness = cleaned_data.get("instrumentalness")
        liveness = cleaned_data.get("liveness")
        valence = cleaned_data.get("valence")
        tempo = cleaned_data.get("tempo")
        
        if popularity < 0 or popularity > 100:
            self.add_error('popularity', 'Popularity must be between 0 and 100.')
        
        if danceability is not None and (danceability < 0.0 or danceability > 1.0):
            self.add_error('danceability', 'Danceability must be between 0.0 and 1.0.')

        if energy is not None and (energy < 0.0 or energy > 1.0):
            self.add_error('energy', 'Energy must be between 0.0 and 1.0.')
            
        if loudness is not None and (loudness > 0.0):
            self.add_error('loudness', 'Loudness must be below 0.0.')
            
        if speechiness is not None and (speechiness < 0.0 or speechiness > 1.0):
            self.add_error('speechiness', 'Speechiness must be between 0.0 and 1.0.')
            
        if acousticness is not None and (acousticness < 0.0 or acousticness > 1.0):
            self.add_error('acousticness', 'Acousticness must be between 0.0 and 1.0.')
            
        if instrumentalness is not None and (instrumentalness < 0.0 or instrumentalness > 1.0):
            self.add_error('instrumentalness', 'Instrumentalness must be between 0.0 and 1.0.')
            
        if liveness is not None and (liveness < 0.0 or liveness > 1.0):
            self.add_error('liveness', 'Liveness must be between 0.0 and 1.0.')
            
        if valence is not None and (valence < 0.0 or valence > 1.0):
            self.add_error('valence', 'Valence must be between 0.0 and 1.0.')
            
        if tempo is not None and (tempo < 0.0 or tempo > 300.0):
            self.add_error('tempo', 'Tempo must be between 0.0 and 300.0.')

        return cleaned_data
    
    class Meta:
        model = Tracks
        fields = [
            'track_name', 
            'artists', 
            'album', 
            'genre', 
            'popularity', 
            'duration_ms', 
            'explicit', 
            'danceability', 
            'energy', 
            'key', 
            'loudness', 
            'mode', 
            'speechiness', 
            'acousticness', 
            'instrumentalness', 
            'liveness', 
            'valence', 
            'tempo', 
            'time_signature'
        ]
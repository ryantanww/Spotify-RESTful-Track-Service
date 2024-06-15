from rest_framework import serializers
from .models import Tracks

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracks
        fields = '__all__'
        
    def validate_track_name(self, value):
        if not isinstance(value, str) or not value:
            raise serializers.ValidationError("Album name must be provided.")
        return value
    
    def validate_artists(self, value):
        if not isinstance(value, str) or not value:
            raise serializers.ValidationError("Artists name must be provided.")
        if ';' in value:
            artists_list = value.split(';')
            for artist in artists_list:
                if not artist.strip():
                    raise serializers.ValidationError("If there are multiple artists, Artists name must be provided after the semi-colon.")
        return value

    def validate_album(self, value):
        if not isinstance(value, str) or not value:
            raise serializers.ValidationError("Album name must be provided.")
        return value
    
    def validate_genre(self, value):
        if not isinstance(value, str) or not value:
            raise serializers.ValidationError("Track genre must be provided.")
        return value
    
    def validate_popularity(self, value):
        if not (0 <= value <= 100):
            raise serializers.ValidationError("Popularity must be between 0 and 100.")
        return value
    
    def validate_duration_ms(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be a positive number.")
        return value
    
    def validate_explicit(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("Explicit must be a boolean value.")
        return value
    
    def validate_danceability(self, value):
        if not (0.0 <= value <= 1.0):
            raise serializers.ValidationError("Danceability must be between 0.0 and 1.0.")
        return value
    
    def validate_energy(self, value):
        if not (0.0 <= value <= 1.0):
            raise serializers.ValidationError("Energy must be between 0.0 and 1.0.")
        return value
    
    def validate_key(self, value):
        if not (-1 <= value <= 11):
            raise serializers.ValidationError("Key must be between -1 and 11.")
        return value
    
    def validate_loudness(self, value):
        try:
            value = float(value)
        except ValueError:
            raise serializers.ValidationError("Loudness must be a number.")
        return value
    
    def validate_mode(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("Mode must be 0 (minor) or 1 (major).")
        return value
    
    def validate_speechiness(self, value):
        if not (0.0 <= value <= 1.0):
            raise serializers.ValidationError("Speechiness must be between 0.0 and 1.0.")
        return value
    
    def validate_acousticness(self, value):
        if not (0.0 <= value <= 1.0):
            raise serializers.ValidationError("Acousticness must be between 0.0 and 1.0.")
        return value

    def validate_instrumentalness(self, value):
        if not (0.0 <= value <= 1.0):
            raise serializers.ValidationError("Instrumentalness must be between 0.0 and 1.0.")
        return value

    def validate_liveness(self, value):
        if not (0.0 <= value <= 1.0):
            raise serializers.ValidationError("Liveness must be between 0.0 and 1.0.")
        return value

    def validate_valence(self, value):
        if not (0.0 <= value <= 1.0):
            raise serializers.ValidationError("Valence must be between 0.0 and 1.0.")
        return value

    def validate_tempo(self, value):
        if value <= 0:
            raise serializers.ValidationError("Tempo must be a positive number.")
        return value

    def validate_time_signature(self, value):
        if not (3 <= value <= 7):
            raise serializers.ValidationError("Time signature must be between 3 and 7.")
        return value

class TrackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracks
        fields = ['id', 'track_name', 'artists']
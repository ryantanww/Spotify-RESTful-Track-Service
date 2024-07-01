from rest_framework import serializers
from .models import Tracks

# Defines a serializer class for the Tracks model
class TrackSerializer(serializers.ModelSerializer):
    # Meta class to specify model and fields to include in the serializer
    class Meta:
        # Link the Tracks model to the serializer
        model = Tracks
        # Included all the fields from the Tracks model
        fields = '__all__'
        # Provide help text for fields so that users will be able to understand what to key in
        extra_kwargs = {
            'track_name': {'help_text': 'Name of the track'},
            'artists': {'help_text': 'Names of the artists, separated by ; if there are multiple'},
            'album': {'help_text': 'Name of the album'},
            'genre': {'help_text': 'Genre of the track'},
            'popularity': {'help_text': 'Popularity of the track (0-100)'},
            'duration_ms': {'help_text': 'Duration of the track in milliseconds'},
            'explicit': {'help_text': 'Indicates whether the track has explicit lyrics'},
            'danceability': {'help_text': 'Suitability of the track for dancing (0.0 to 1.0)'},
            'energy': {'help_text': 'Intensity and activity of the track (0.0 to 1.0)'},
            'key': {'help_text': 'The key the track is in (0-11) What pitch it contains, if there is no key, the value can be -1'},
            'loudness': {'help_text': 'Overall loudness of the track in decibels (dB)'},
            'mode': {'help_text': 'Modality of the track (0 for minor, 1 for major)'},
            'speechiness': {'help_text': 'Presence of spoken words in the track (0.0 to 1.0)'},
            'acousticness': {'help_text': 'Confidence measure whether the track is acoustic (0.0 to 1.0)'},
            'instrumentalness': {'help_text': 'Likelihood the track contains no vocals (0.0 to 1.0)'},
            'liveness': {'help_text': 'Presence of an audience in the recording (0.0 to 1.0)'},
            'valence': {'help_text': 'Positiveness conveyed by the track (0.0 to 1.0)'},
            'tempo': {'help_text': 'Estimated tempo of the track in BPM'},
            'time_signature': {'help_text': 'Estimated time signature of the track (3-7)'},
        }
        
    # Method to validate track_name
    def validate_track_name(self, value):
        # Ensures that track_name is not an empty string value
        if not isinstance(value, str) or not value:
            # Raises a validation error if track_name is an empty string value
            raise serializers.ValidationError("Track name must be provided.")
        
        # Returns validated track_name
        return value
    
    # Method to validate artists name
    def validate_artists(self, value):
        # Ensures that artists is not an empty string value
        if not isinstance(value, str) or not value:
            # Raises a validation error if artists is an empty string value
            raise serializers.ValidationError("Artists name must be provided.")
        
        # If there are multiple artists, validate each one separated by the ';'
        if ';' in value:
            # Split artists by the ';'
            artists_list = value.split(';')
            # For each artist in the list
            for artist in artists_list:
                # Check if the artist name is empty or contains only whitespace
                if not artist.strip():
                    # Raises a validation error if artists is an empty string value or only whitespace
                    raise serializers.ValidationError("If there are multiple artists, Artists name must be provided after the semi-colon.")
        
        # Returns validated artists
        return value

    # Method to validate album name
    def validate_album(self, value):
        # Ensures that album is not an empty string value
        if not isinstance(value, str) or not value:
            # Raises a validation error if album is an empty string value
            raise serializers.ValidationError("Album name must be provided.")
        
        # Returns validated album
        return value
    
    # Method to validate genre
    def validate_genre(self, value):
        # Ensures that genre is not an empty string value
        if not isinstance(value, str) or not value:
            # Raises a validation error if genre is an empty string value
            raise serializers.ValidationError("Track genre must be provided.")
        
        # Returns validated genre
        return value
    
    # Method to validate popularity
    def validate_popularity(self, value):
        # Ensures that popularity is between 0 and 100
        if not (0 <= value <= 100):
            # Raises a validation error if popularity is not between 0 and 100
            raise serializers.ValidationError("Popularity must be between 0 and 100.")
        
        # Returns validated popularity
        return value
    
    # Method to validate duration_ms
    def validate_duration_ms(self, value):
        # Ensures that duration_ms is a positive number
        if value <= 0:
            # Raises a validation error if duration_ms is not a positive number
            raise serializers.ValidationError("Duration must be a positive number.")
        
        # Returns validated duration_ms
        return value
    
    # Method to validate explicit
    def validate_explicit(self, value):
        # Ensures that explicit is a boolean value
        if not isinstance(value, bool):
            # Raises a validation error if explicit is not a boolean value
            raise serializers.ValidationError("Explicit must be a boolean value.")
        
        # Returns validated explicit
        return value
    
    # Method to validate danceability
    def validate_danceability(self, value):
        # Ensures that danceability is between 0.0 and 1.0
        if not (0.0 <= value <= 1.0):
            # Raises a validation error if danceability is not between 0.0 and 1.0
            raise serializers.ValidationError("Danceability must be between 0.0 and 1.0.")
        
        # Returns validated danceability
        return value
    
    # Method to validate energy
    def validate_energy(self, value):
        # Ensures that energy is between 0.0 and 1.0
        if not (0.0 <= value <= 1.0):
            # Raises a validation error if track_name is not between 0.0 and 1.0
            raise serializers.ValidationError("Energy must be between 0.0 and 1.0.")
        
        # Returns validated energy
        return value
    
    # Method to validate  key
    def validate_key(self, value):
        # Ensures that key is between -1 and 11
        if not (-1 <= value <= 11):
            # Raises a validation error if key is not between -1 and 11
            raise serializers.ValidationError("Key must be between -1 and 11.")
        
        # Returns validated key
        return value
    
    # Method to validate loudness
    def validate_loudness(self, value):
        
        try:
            # Ensures that loudness is a number
            value = float(value)
        except ValueError:
            # Raises a validation error if loudness is not a number
            raise serializers.ValidationError("Loudness must be a number.")
        
        # Returns validated loudness
        return value
    
    # Method to validate mode
    def validate_mode(self, value):
        # Ensures that mode is either 0 or 1
        if value not in [0, 1]:
            # Raises a validation error if mode is not 0 or 1
            raise serializers.ValidationError("Mode must be 0 (minor) or 1 (major).")
        
        # Returns validated mode
        return value
    
    # Method to validate speechiness
    def validate_speechiness(self, value):
        # Ensures that speechiness is between 0.0 and 1.0
        if not (0.0 <= value <= 1.0):
            # Raises a validation error if speechiness is not between 0.0 and 1.0
            raise serializers.ValidationError("Speechiness must be between 0.0 and 1.0.")
        
        # Returns validated speechiness
        return value
    
    # Method to validate acousticness
    def validate_acousticness(self, value):
        # Ensures that acousticness is between 0.0 and 1.0
        if not (0.0 <= value <= 1.0):
            # Raises a validation error if acousticness is not between 0.0 and 1.0
            raise serializers.ValidationError("Acousticness must be between 0.0 and 1.0.")
        
        # Returns validated acousticness
        return value

    # Method to validate instrumentalness
    def validate_instrumentalness(self, value):
        # Ensures that instrumentalness is between 0.0 and 1.0
        if not (0.0 <= value <= 1.0):
            # Raises a validation error if instrumentalness is not between 0.0 and 1.0
            raise serializers.ValidationError("Instrumentalness must be between 0.0 and 1.0.")
        
        # Returns validated instrumentalness
        return value

    # Method to validate liveness
    def validate_liveness(self, value):
        # Ensures that liveness is between 0.0 and 1.0
        if not (0.0 <= value <= 1.0):
            # Raises a validation error if liveness is not between 0.0 and 1.0
            raise serializers.ValidationError("Liveness must be between 0.0 and 1.0.")
        
        # Returns validated liveness
        return value

    # Method to validate valence
    def validate_valence(self, value):
        # Ensures that valence is between 0.0 and 1.0
        if not (0.0 <= value <= 1.0):
            # Raises a validation error if valence is not between 0.0 and 1.0
            raise serializers.ValidationError("Valence must be between 0.0 and 1.0.")
        
        # Returns validated valence
        return value

    # Method to validate tempo
    def validate_tempo(self, value):
        # Ensures that tempo is a positive number
        if value <= 0:
            # Raises a validation error if tempo is not a positive number
            raise serializers.ValidationError("Tempo must be a positive number.")
        
        # Returns validated tempo
        return value

    # Method to validate time_signature
    def validate_time_signature(self, value):
        # Ensures that time_signature is between 3 and 7
        if not (3 <= value <= 7):
            # Raises a validation error if time_signature is not between 3 and 7
            raise serializers.ValidationError("Time signature must be between 3 and 7.")
        
        # Returns validated time_signature
        return value

# Defines a serializer for listing tracks with limited fields
class TrackListSerializer(serializers.ModelSerializer):
    # Meta class to specify model and fields to include in the serializer
    class Meta:
        # Link the Tracks model to the serializer
        model = Tracks
        # Include only the id, track_name and artists fields from the Tracks model
        fields = ['id', 'track_name', 'artists']
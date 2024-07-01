from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

# Retrieves a list of tracks filtered by genre for users to find tracks in the specific genres
@api_view(['GET'])
def tracks_by_genre(request, genre):
    # Query the database to filter tracks based on the genre
    tracks = Tracks.objects.filter(genre=genre)
    # Serialize the list of tracks
    serializer = TrackSerializer(tracks, many=True)
    # Return the serialized data as a JSON response
    return Response(serializer.data)

# Retrieves a list of popular tracks filtered by a popularity threshold and shown in descending order for users to find popular tracks
@api_view(['GET'])
def popular_tracks(request):
    # Get popularity threshold from query parameters, defaulted to 80 if not provided
    popularity_threshold = int(request.query_params.get('popularity', 80))
    
    # Query the database to filter tracks based on the popularity greater than or equal to the threhold
    # and sort in descending order
    tracks = Tracks.objects.filter(popularity__gte=popularity_threshold).order_by('-popularity')

    # Serialize the list of tracks
    serializer = TrackSerializer(tracks, many=True)
    # Return the serialized data as a JSON response
    return Response(serializer.data)

# Retrieves a list of tracks with high danceability and within a tempo range for users to find the better tracks to dance to
@api_view(['GET'])
def high_danceability_tracks(request):
    # Get danceability threshold from query parameters, defaulted to 0.8 if not provided
    danceability_threshold = float(request.query_params.get('danceability', 0.8))
    # Get minimum tempo threshold from query parameters, defaulted to 90.0 if not provided
    min_tempo = float(request.query_params.get('min_tempo', 90.0))
    # Get maximum tempo threshold from query parameters, defaulted to 130.0 if not provided
    max_tempo = float(request.query_params.get('max_tempo', 130.0))

    # Query the database to filter tracks based on danceability and tempo
    tracks = Tracks.objects.filter(
            danceability__gte=danceability_threshold, 
            tempo__gte=min_tempo,
            tempo__lte=max_tempo
        )

    # Serialize the list of tracks
    serializer = TrackSerializer(tracks, many=True)
    # Return the serialized data as a JSON response
    return Response(serializer.data)

# API view to create a new track
class CreateTrack(mixins.CreateModelMixin,
                    generics.GenericAPIView):
    # Defines the queryset to use for this view
    queryset = Tracks.objects.all()
    # Defines the serializer class to use for this view
    serializer_class = TrackSerializer

    # Handles the POST request to create a new track
    def post(self, request, *args, **kwargs):
        # Deserialize the incoming data into a serializer instance
        serializer = self.get_serializer(data=request.data)
        # Validate the data
        serializer.is_valid(raise_exception=True)
        # Save the new track to the database
        self.perform_create(serializer)
        # Return the serialized data with a HTTP 201 Created status
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# API view to retrieve, update or delete a track by ID
class TrackDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    # Defines the queryset to use for this view
    queryset = Tracks.objects.all()
    # Defines the serializer class to use for this view
    serializer_class = TrackSerializer

    # Handles the GET request to retrieve a track by ID
    def get(self, request, *args, **kwargs):
        # Retrieve and return the track data
        return self.retrieve(request, *args, **kwargs)

    # Handles the PUT request to update a track by ID
    def put(self, request, *args, **kwargs):
        # Checks if the update should be partial or not
        partial = kwargs.pop('partial', False)
        # Get the track instance to update
        instance = self.get_object()
        # Deserialize the incoming data into a serializer instance
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # Validate the data
        serializer.is_valid(raise_exception=True)
        # Save the updated track to the database
        self.perform_update(serializer)
        # Return the serialized data
        return Response(serializer.data)

    # Handles the DELETE request to delete a track by ID
    def delete(self, request, *args, **kwargs):
        # Deletes the track's instance
        return self.destroy(request, *args, **kwargs)
    

# API view to list the ID, name and artists names of all the tracks in the database
class TrackList(generics.ListAPIView):
    # Defines the queryset to use for this view
    queryset = Tracks.objects.all()
    # Defines the serializer class to use for this view
    serializer_class = TrackListSerializer
    


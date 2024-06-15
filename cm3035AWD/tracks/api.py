from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

@api_view(['GET'])
def tracks_by_genre(request, genre):
    tracks = Tracks.objects.filter(genre=genre)
    serializer = TrackSerializer(tracks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def popular_tracks(request):
    # Get threshold from query parameters, with default if not provided
    popularity_threshold = int(request.query_params.get('popularity', 50))

    # Filter tracks based on the threshold
    tracks = Tracks.objects.filter(popularity__gte=popularity_threshold)

    serializer = TrackSerializer(tracks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def high_energy_danceable_tracks(request):
    # Get thresholds from query parameters, with defaults if not provided
    energy_threshold = float(request.query_params.get('energy', 0.8))
    danceability_threshold = float(request.query_params.get('danceability', 0.8))

    # Filter tracks based on the thresholds
    tracks = Tracks.objects.filter(energy__gte=energy_threshold, danceability__gte=danceability_threshold)

    # Serialize the resulting tracks
    serializer = TrackSerializer(tracks, many=True)
    return Response(serializer.data)

class TrackDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Tracks.objects.all()
    serializer_class = TrackSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class TrackList(generics.ListAPIView):
    queryset = Tracks.objects.all()
    serializer_class = TrackListSerializer
    


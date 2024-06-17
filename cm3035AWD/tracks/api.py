from rest_framework import generics, mixins, status
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
    popularity_threshold = int(request.query_params.get('popularity', 80)) # sort in ascending order instead
    
    # Filter tracks based on the threshold
    tracks = Tracks.objects.filter(popularity__gte=popularity_threshold).order_by('-popularity')

    serializer = TrackSerializer(tracks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def high_danceability_tracks(request):
    # Get thresholds from query parameters, with defaults if not provided
    danceability_threshold = float(request.query_params.get('danceability', 0.8))
    min_tempo = float(request.query_params.get('min_tempo', 90.0))
    max_tempo = float(request.query_params.get('max_tempo', 130.0))

    # Filter tracks based on the thresholds
    tracks = Tracks.objects.filter(
            danceability__gte=danceability_threshold, 
            tempo__gte=min_tempo,
            tempo__lte=max_tempo
        )

    # Serialize the resulting tracks
    serializer = TrackSerializer(tracks, many=True)
    return Response(serializer.data)

class CreateTrack(mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Tracks.objects.all()
    serializer_class = TrackSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class TrackDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Tracks.objects.all()
    serializer_class = TrackSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class TrackList(generics.ListAPIView):
    queryset = Tracks.objects.all()
    serializer_class = TrackListSerializer
    


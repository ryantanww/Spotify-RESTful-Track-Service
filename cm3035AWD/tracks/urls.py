from django.urls import path
from django.views.generic import TemplateView
from . import views
from . import api

# URL patterns for the tracks application
urlpatterns = [
    # URL patter for the index page, displaying necessary information
    path('', TemplateView.as_view(template_name='tracks\index.html'), name='index'),
    
    # URL pattern for listing all tracks using the TrackList API
    path('api/tracks/', api.TrackList.as_view(), name='tracks_list_api'),
    
    # URL pattern for creating new track through the CreateTrack API
    path('api/tracks/create_track/', api.CreateTrack.as_view(), name='create_track_api'),
    
    # URL pattern for retreiving, updating and deleted a track via the primary key through the TrackDetail API
    path('api/tracks/<int:pk>/', api.TrackDetail.as_view(), name='track_detail_api'),
    
    # URL pattern for listing all tracks filtered by genre using the tracks_by_genre API
    path('api/tracks/genre/<str:genre>/', api.tracks_by_genre, name='tracks_by_genre_api'),
    
    # URL pattern for listing all tracks filtered by popularity using the popular_tracks API
    path('api/tracks/popular_tracks/', api.popular_tracks, name='popular_tracks_api'),
    
    # URL pattern for listing all tracks filtered by dancebility and tempo using the high_danceability_tracks API
    path('api/tracks/high_danceability_tracks/', api.high_danceability_tracks, name='high_danceability_tracks_api'),
]
from django.urls import path
from django.views.generic import TemplateView
from . import views
from . import api

urlpatterns = [
    path('', TemplateView.as_view(template_name='tracks\index.html'), name='index'),
    path('api/', api.TrackList.as_view(), name='tracks_list_api'),
    path('api/create/', api.CreateTrack.as_view(), name='create_track'),
    path('api/<int:pk>/', api.TrackDetail.as_view(), name='track_detail_api'),
    path('api/genre/<str:genre>/', api.tracks_by_genre, name='tracks_by_genre'),
    path('api/popular_tracks/', api.popular_tracks, name='popular_tracks'),
    path('api/high_danceability_tracks/', api.high_danceability_tracks, name='high_danceability_tracks'),
]
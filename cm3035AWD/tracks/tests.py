import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .model_factories import TracksFactory
from .serializers import *
from .models import *

from decimal import Decimal

class TrackSerializerTest(APITestCase):

    def setUp(self):
        self.track = TracksFactory()
        self.track_serializer = TrackSerializer(instance=self.track)

    def tearDown(self):
        Tracks.objects.all().delete()

    def test_track_serializer_has_correct_fields(self):
        data = self.track_serializer.data
        self.assertEqual(set(data.keys()), {
            'id', 'track_name', 'artists', 'album', 'genre', 'popularity', 
            'duration_ms', 'explicit', 'danceability', 'energy', 'key', 
            'loudness', 'mode', 'speechiness', 'acousticness', 
            'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature'
        })

    def test_track_serializer_track_name_has_correct_data(self):
        data = self.track_serializer.data
        self.assertEqual(data['track_name'], self.track.track_name)
        
    def test_track_serializer_genre_has_correct_data(self):
        data = self.track_serializer.data
        self.assertEqual(data['genre'], self.track.genre)
    
    def test_track_serializer_popularity_has_correct_data(self):
        data = self.track_serializer.data
        self.assertEqual(data['popularity'], self.track.popularity)
        
    def test_track_serializer_danceability_has_correct_data(self):
        data = self.track_serializer.data
        self.assertEqual(Decimal(data['danceability']), self.track.danceability)
        
    def test_track_serializer_tempo_has_correct_data(self):
        data = self.track_serializer.data
        self.assertEqual(Decimal(data['tempo']), self.track.tempo)

class TrackAPITest(APITestCase):

    def setUp(self):
        self.track1 = TracksFactory(popularity=85, danceability=0.925, tempo=92.015, genre='Disco')
        self.track2 = TracksFactory(popularity=75, danceability=0.671, tempo=113.506, genre='Pop')
        self.track3 = TracksFactory(popularity=90, danceability=0.954, tempo=121.836, genre='Disco')
        self.track_list_url = reverse('tracks_list_api')
        self.track_detail_url = reverse('track_detail_api', kwargs={'pk': self.track1.id})
        self.track_update_detail_url = reverse('track_detail_api', kwargs={'pk': self.track2.id})
        self.bad_url = '/api/tracks/fail/'
        self.create_track_url = reverse('create_track_api')
        self.tracks_by_genre_url = reverse('tracks_by_genre_api', kwargs={'genre': self.track1.genre})
        self.popular_tracks_url = reverse('popular_tracks_api')
        self.high_danceability_tracks_url = reverse('high_danceability_tracks_api')
        

    def tearDown(self):
        Tracks.objects.all().delete()
        
    def test_track_list_returns_success(self):
        response = self.client.get(self.track_list_url, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)

    def test_track_detail_returns_success(self):
        response = self.client.get(self.track_detail_url, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('track_name' in data)
        
    def test_bad_url_returns_fail(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)

    def test_create_track(self):
        data = {
            'track_name': 'Create New Track',
            'artists': 'Tester',
            'album': 'Test',
            'genre': 'Disco',
            'popularity': 58,
            'duration_ms': 400115,
            'explicit': False,
            'danceability': 0.82,
            'energy': 0.478,
            'key': 5,
            'loudness': -5.896,
            'mode': 1,
            'speechiness': 0.224,
            'acousticness': 0.38,
            'instrumentalness': 0.14,
            'liveness': 0.41,
            'valence': 0.77,
            'tempo': 105.14,
            'time_signature': 4
        }
        response = self.client.post(self.create_track_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['track_name'], 'Create New Track')
        self.assertEqual(response.data['genre'], 'Disco')
        self.assertEqual(response.data['popularity'], 58)
        self.assertEqual(response.data['explicit'], False)
        self.assertEqual(response.data['key'], 5)
        self.assertEqual(Decimal(response.data['danceability']), Decimal('0.820'))
        self.assertEqual(Decimal(response.data['tempo']), Decimal('105.140'))

    def test_tracks_by_genre(self):
        response = self.client.get(self.tracks_by_genre_url, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)
        for track in data:
            self.assertEqual(track['genre'], self.track1.genre)
            
    def test_popular_tracks(self):
        response = self.client.get(self.popular_tracks_url, {'popularity': 80}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)
        for track in data:
            self.assertGreaterEqual(track['popularity'], 80)
            
    def test_high_danceability_tracks(self):
        response = self.client.get(self.high_danceability_tracks_url, {'danceability': 0.8, 'min_tempo': 90.0, 'max_tempo': 130.0}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)
        for track in data:
            self.assertGreaterEqual(Decimal(track['danceability']), Decimal('0.800'))
            self.assertGreaterEqual(Decimal(track['tempo']), Decimal('90.000'))
            self.assertLessEqual(Decimal(track['tempo']), Decimal('130.000'))
            
    def test_popular_tracks_threshold(self):
        response = self.client.get(self.popular_tracks_url, {'popularity': 70}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)
        for track in data:
            self.assertGreaterEqual(track['popularity'], 70)

    def test_high_danceability_tracks_different_thresholds(self):
        response = self.client.get(self.high_danceability_tracks_url, {'danceability': 0.7, 'min_tempo': 100.0, 'max_tempo': 130.0}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)
        for track in data:
            self.assertGreaterEqual(Decimal(track['danceability']), Decimal('0.700'))
            self.assertGreaterEqual(Decimal(track['tempo']), Decimal('100.000'))
            self.assertLessEqual(Decimal(track['tempo']), Decimal('130.000'))
            
    def test_update_track(self):
        update_data = {
            'track_name': 'Updated Track',
            'artists': 'Updated Artist',
            'album': 'Updated Album',
            'genre': 'Updated Genre',
            'popularity': 60,
            'duration_ms': 250000,
            'explicit': True,
            'danceability': 0.7,
            'energy': 0.6,
            'key': 4,
            'loudness': -4.0,
            'mode': 0,
            'speechiness': 0.2,
            'acousticness': 0.2,
            'instrumentalness': 0.1,
            'liveness': 0.2,
            'valence': 0.6,
            'tempo': 115.0,
            'time_signature': 5
        }
        response = self.client.put(self.track_detail_url, update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['track_name'], 'Updated Track')
        self.assertEqual(response.data['artists'], 'Updated Artist')
        self.assertEqual(response.data['album'], 'Updated Album')
        self.assertEqual(response.data['genre'], 'Updated Genre')
        self.assertEqual(response.data['popularity'], 60)
        self.assertEqual(response.data['duration_ms'], 250000)
        self.assertEqual(response.data['explicit'], True)
        self.assertEqual(Decimal(response.data['danceability']), Decimal('0.700'))
        self.assertEqual(Decimal(response.data['energy']), Decimal('0.600'))
        self.assertEqual(response.data['key'], 4)
        self.assertEqual(Decimal(response.data['loudness']), Decimal('-4.000'))
        self.assertEqual(response.data['mode'], 0)
        self.assertEqual(Decimal(response.data['speechiness']), Decimal('0.200'))
        self.assertEqual(Decimal(response.data['acousticness']), Decimal('0.200'))
        self.assertEqual(Decimal(response.data['instrumentalness']), Decimal('0.10000'))
        self.assertEqual(Decimal(response.data['liveness']), Decimal('0.200'))
        self.assertEqual(Decimal(response.data['valence']), Decimal('0.600'))
        self.assertEqual(Decimal(response.data['tempo']), Decimal('115.000'))
        self.assertEqual(response.data['time_signature'], 5)

    def test_track_delete(self):
        response = self.client.delete(reverse('track_detail_api', kwargs={'pk': self.track3.id}), format='json')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Tracks.objects.filter(pk=self.track3.id).exists())
        
        

import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .model_factories import TracksFactory
from .serializers import *
from .models import *

from decimal import Decimal

# Test case class for testing the TrackSerializer
class TrackSerializerTest(APITestCase):

    # Setup method to create test data for the test environment
    def setUp(self):
        self.track = TracksFactory()
        self.track_serializer = TrackSerializer(instance=self.track)

    # Teardown method to clean up after each test
    def tearDown(self):
        Tracks.objects.all().delete()

    # Test to check if TrackSerializer has all expected fields
    def test_track_serializer_has_correct_fields(self):
        data = self.track_serializer.data
        self.assertEqual(set(data.keys()), {
            'id', 'track_name', 'artists', 'album', 'genre', 'popularity', 
            'duration_ms', 'explicit', 'danceability', 'energy', 'key', 
            'loudness', 'mode', 'speechiness', 'acousticness', 
            'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature'
        })

    # Test to verify if TrackSerializer correctly serializes the track_name
    def test_track_serializer_track_name_has_correct_data(self):
        data = self.track_serializer.data
        self.assertEqual(data['track_name'], self.track.track_name)
    
    # Test to verify if TrackSerializer correctly serializes the genre
    def test_track_serializer_genre_has_correct_data(self):
        data = self.track_serializer.data
        self.assertEqual(data['genre'], self.track.genre)
    
    # Test to verify if TrackSerializer correctly serializes the popularity
    def test_track_serializer_popularity_has_correct_data(self):
        data = self.track_serializer.data
        self.assertEqual(data['popularity'], self.track.popularity)
    
    # Test to verify if TrackSerializer correctly serializes the danceability
    def test_track_serializer_danceability_has_correct_data(self):
        data = self.track_serializer.data
        self.assertEqual(Decimal(data['danceability']), self.track.danceability)
    
    # Test to verify if TrackSerializer correctly serializes the tempo
    def test_track_serializer_tempo_has_correct_data(self):
        data = self.track_serializer.data
        self.assertEqual(Decimal(data['tempo']), self.track.tempo)

# Test case class for testing the Tracks API endpoints
class TrackAPITest(APITestCase):

    # Setup method to create test data for the test environment
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
        
    # Teardown method to clean up after each test
    def tearDown(self):
        Tracks.objects.all().delete()
        
    # Test to verify if retrieving all tracks from TrackList API works correctly
    def test_track_list_returns_success(self):
        # Sends a GET request to TrackList API and checks if response status code is 200
        response = self.client.get(self.track_list_url, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Loads response as JSON and checks if response contains data
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)

    # Test to verify if retrieving a track through TrackDetail API works correctly
    def test_track_detail_returns_success(self):
        # Sends a GET request to TrackDetail API and checks if response status code is 200
        response = self.client.get(self.track_detail_url, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Loads response as JSON and checks if track_name is present
        data = json.loads(response.content)
        self.assertTrue('track_name' in data)
    
    # Test to verify if providing a wrong URL returns a 404 (Not Found) response
    def test_bad_url_returns_fail(self):
        # Send GET request for wrong URL and checks if the response status code is 404
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)

    # Test to verify if creating a new track through CreateTrack API works correctly
    def test_create_track(self):
        # Data for creating a track
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
        
        # Sends a POST request to CreateTrack API and checks if response status code is 201
        response = self.client.post(self.create_track_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        
        # Checks if the returned data matches the posted data
        self.assertEqual(response.data['track_name'], 'Create New Track')
        self.assertEqual(response.data['genre'], 'Disco')
        self.assertEqual(response.data['popularity'], 58)
        self.assertEqual(response.data['explicit'], False)
        self.assertEqual(Decimal(response.data['danceability']), Decimal('0.820'))
        self.assertEqual(response.data['key'], 5)
        self.assertEqual(Decimal(response.data['tempo']), Decimal('105.140'))

    # Test to verify if tracks_by_genre API returns tracks with correct genre
    def test_tracks_by_genre(self):
        # Sends a GET request to tracks_by_genre API and checks if response status code is 200
        response = self.client.get(self.tracks_by_genre_url, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Loads response as JSON and checks if response contains data
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)
        # Checks if each track's genre matches track1's genre
        for track in data:
            self.assertEqual(track['genre'], self.track1.genre)
            
    # Test to verify if popular_tracks API returns tracks with popularity greater than or equal to 80 (default)
    def test_popular_tracks(self):
        # Sends a GET request to popular_tracks API and checks if response status code is 200
        response = self.client.get(self.popular_tracks_url, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Loads response as JSON and checks if response contains data
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)
        # Checks if each track's popularity is greater than or equal to 80
        for track in data:
            self.assertGreaterEqual(track['popularity'], 80)
    
    # Test to verify if high_danceability_tracks API returns tracks with danceability greater than or equal 0.8 and tempo between 90 and 130 (default)
    def test_high_danceability_tracks(self):
        # Sends a GET request to high_danceability_tracks API and checks if response status code is 200
        response = self.client.get(self.high_danceability_tracks_url, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Loads response as JSON and checks if response contains data
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)
        # Checks if each track's danceaility and tempo is in the correct range
        for track in data:
            self.assertGreaterEqual(Decimal(track['danceability']), Decimal('0.800'))
            self.assertGreaterEqual(Decimal(track['tempo']), Decimal('90.000'))
            self.assertLessEqual(Decimal(track['tempo']), Decimal('130.000'))
    
    # Test to verify if popular_tracks API returns tracks with popularity greater than or equal to 70
    def test_popular_tracks_different_threshold(self):
        # Sends a GET request to popular_tracks API and checks if response status code is 200
        response = self.client.get(self.popular_tracks_url, {'popularity': 70}, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Loads response as JSON and checks if response contains data
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)
        # Checks if each track's popularity is greater than or equal to 70
        for track in data:
            self.assertGreaterEqual(track['popularity'], 70)

    # Test to verify if high_danceability_tracks API returns tracks with danceability greater than or equal 0.7 and tempo between 100 and 140
    def test_high_danceability_tracks_different_thresholds(self):
        # Sends a GET request to high_danceability_tracks API and checks if response status code is 200
        response = self.client.get(self.high_danceability_tracks_url, {'danceability': 0.7, 'min_tempo': 100.0, 'max_tempo': 140.0}, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Loads response as JSON and checks if response contains data
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)
        # Checks if each track's danceaility and tempo is in the correct range
        for track in data:
            self.assertGreaterEqual(Decimal(track['danceability']), Decimal('0.700'))
            self.assertGreaterEqual(Decimal(track['tempo']), Decimal('100.000'))
            self.assertLessEqual(Decimal(track['tempo']), Decimal('140.000'))
    
    # Test to verify if updating a track through TrackDetail API works correctly
    def test_update_track(self):
        # Data for updating a track
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
        # Sends a PUT request to TrackDetail API and checks if response status code is 200
        response = self.client.put(self.track_detail_url, update_data, format='json')
        self.assertEqual(response.status_code, 200)
        # Checks if the returned data matches the updated data
        self.assertEqual(response.data['track_name'], 'Updated Track')
        self.assertEqual(response.data['genre'], 'Updated Genre')
        self.assertEqual(response.data['popularity'], 60)
        self.assertEqual(response.data['explicit'], True)
        self.assertEqual(Decimal(response.data['danceability']), Decimal('0.700'))
        self.assertEqual(response.data['key'], 4)
        self.assertEqual(Decimal(response.data['tempo']), Decimal('115.000'))

    # Test to verify if deleting a track through TrackDetail API works correctly
    def test_track_delete(self):
        # Sends a DELETE request to TrackDetail API and checks if response status codes is 204
        response = self.client.delete(reverse('track_detail_api', kwargs={'pk': self.track3.id}), format='json')
        self.assertEqual(response.status_code, 204)
        
        # Checks if track3 still exists in the database
        self.assertFalse(Tracks.objects.filter(pk=self.track3.id).exists())
        
        

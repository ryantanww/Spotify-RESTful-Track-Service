import factory
from .models import *

# Defines a factory for creating instances of the Tracks model for testing
class TracksFactory(factory.django.DjangoModelFactory):
    # Meta class to specify the model to include in the factory
    class Meta:
        # Link the Tracks model to the factory
        model = Tracks
    
    # Defines the default values for the Tracks model when creating instances for testing using Faker
    track_name = factory.Faker('word')
    artists = factory.Faker('name')
    album = factory.Faker('word')
    genre = factory.Faker('word')
    popularity = factory.Faker('random_int', min=0, max=100)
    duration_ms = factory.Faker('random_int', min=1, max=500000)
    explicit = factory.Faker('boolean')
    danceability = factory.Faker('pydecimal', left_digits=1, right_digits=3, positive=True)
    energy = factory.Faker('pydecimal', left_digits=1, right_digits=3, positive=True)
    key = factory.Faker('random_int', min=-1, max=11)
    loudness = factory.Faker('pydecimal', left_digits=2, right_digits=3, positive=False)
    mode = factory.Faker('random_int', min=0, max=1)
    speechiness = factory.Faker('pydecimal', left_digits=1, right_digits=3, positive=True)
    acousticness = factory.Faker('pydecimal', left_digits=1, right_digits=3, positive=True)
    instrumentalness = factory.Faker('pydecimal', left_digits=1, right_digits=5, positive=True)
    liveness = factory.Faker('pydecimal', left_digits=1, right_digits=3, positive=True)
    valence = factory.Faker('pydecimal', left_digits=1, right_digits=3, positive=True)
    tempo = factory.Faker('pydecimal', left_digits=3, right_digits=3, positive=True)
    time_signature = factory.Faker('random_int', min=3, max=7)
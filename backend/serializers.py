from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = '__all__'

class AnimeEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeEpisode
        fields = '__all__'
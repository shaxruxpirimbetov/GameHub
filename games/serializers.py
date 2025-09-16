from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game, GameImages


class GameImagesSerializer(serializers.ModelSerializer):
	class Meta:
		model = GameImages
		fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
	images = GameImagesSerializer(many=True, source="gameimages_set")
	class Meta:
		model = Game
		fields = "__all__"



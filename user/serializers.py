from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PlayedGame, PageImage


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = "__all__"


class PlayedGameSerializer(serializers.ModelSerializer):
	class Meta:
		model = PlayedGame
		fields = "__all__"


class PageImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = PageImage
		fields = "__all__"
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import UserSerializer, PlayedGameSerializer, PageImageSerializer
from .models import PlayedGame, PageImage
from games.models import Game
page = ""


class RegisterApi(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		username = request.data.get("username")
		password = request.data.get("password")
		
		user = User.objects.filter(username=username).first()
		if user:
			return Response({"status": False, "message": "User already exists"})
		
		user = User.objects.create_user(username=username, password=password)
		user = UserSerializer(user).data
		return Response(user)


class PlayedGameApi(APIView):
	def get(self, request):
		played_game = PlayedGame.objects.filter(user=request.user)
		played_game = PlayedGameSerializer(played_game).data
		return Response(played_game)

	def post(self, request):
		game_id = request.data.get("game_id")
		if not game_id:
			return Response({"status": False, "message": "game_id is required"})

		game = Game.objects.filter(id=game_id)
		if not game:
			return Response({"status": False, "message": "Game not found"})

		game = PlayedGame.objetcs.create(user=request.user, game=game)
		game = PlayedGameSerializer(game).data
		return Response(game)


class CheckTokenApi(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		return Response({"status": True})


class PageApi(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self, request):
		global page
		return Response({"status": True, "message": "page in page", "page": page})
	
	def post(self, request):
		global page
		page = request.data.get("page")
		if not page:
			return Response({"status": False, "message": "Page are required"})
		
		page = page
		return Response({"status": True, "message": "Page saved successfully"})


class PageImagesApi(APIView):
	permission_classes = [permissions.AllowAny]
	parser_classes = [MultiPartParser, FormParser, JSONParser]
	def get(self, request):
		pages = PageImage.objects.all()
		pages = PageImageSerializer(pages, many=True).data
		return Response(pages)
	
	def post(self, request):
		images = request.FILES.getlist("images")
		for image in images:
			PageImage.objects.create(image=image)
		
		return Response({"status": True, "message": "Yah"})
	


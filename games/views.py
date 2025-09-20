from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import permissions
from rest_framework.views import APIView
import shutil
from .models import Game, GameImages
from .serializers import GameSerializer


class GameApi(APIView):
	parser_classes = [MultiPartParser, FormParser, JSONParser]
	def get_permissions(self):
		if self.request.method == "GET":
			if self.request.GET.get("my"):
				return [permissions.IsAuthenticated()]
			return [permissions.AllowAny()]
		else:
			return [permissions.IsAuthenticated()]

	def get(self, request):
		game_id = request.GET.get("game_id")
		my = request.GET.get("my")
		if game_id:
			game = Game.objects.filter(id=game_id).first()
			if not game:
				return Response({"status": False, "message": "Game not found"})
			game = GameSerializer(game).data
			game["path"] = f"media/games/{game.get('title').replace(' ','').lower()}/{game.get('run_file')}"
			return Response(game)

		if my:
			games = Game.objects.filter(author=request.user).all()
			games = GameSerializer(games, many=True).data
			return Response(games)
		
		games = Game.objects.all()
		games = GameSerializer(games, many=True).data
		# Game.objects.all().delete()
		return Response(games)
	
	def post(self, request):
		title = request.data.get("title")
		description = request.data.get("description")
		run_file = request.data.get("run_file")
		logo = request.FILES.get("logo")
		images = request.FILES.getlist("images")
		file = request.FILES.get("file")
		
		if not all([file, title, description, run_file, logo, images]):
			return Response({"status": False, "message": "Invalid datas"})
		
		gamename = title.lower().replace(" ", "")
		run_path = f"{gamename}/{run_file}"
		game = Game.objects.filter(gamename=gamename).first()
		if game:
			return Response({"status": False, "message": "Game already exists"})
		
		game = Game.objects.create(
		    author=request.user,
		    title=title,
		    gamename=gamename,
		    description=description,
		    run_file=run_file,
		    run_path=run_path,
		    logo=logo
		)
		for image in images:
			GameImages.objects.create(game=game, image=image)
		game = GameSerializer(game).data
		
		shutil.unpack_archive(file.temporary_file_path(), f"media/games/{gamename}")
		return Response(game)
	
	def delete(self, request):
		game_id = request.data.get("game_id")
		if not game_id:
			return Response({"status": False, "message": "game_id are required"})
		
		game = Game.objects.filter(id=game_id).first()
		if not game:
			return Response({"status": False, "message": "Game not found"})
		
		game.delete()
		return Response({"status": True, "message": "Game deleted successfully"})




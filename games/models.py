from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.db import models
import shutil, os


class Game(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	logo = models.ImageField(upload_to="logos/")
	title = models.CharField(max_length=24)
	gamename = models.CharField(max_length=24)
	description = models.TextField()
	run_file = models.TextField()
	run_path = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"Game {self.title}"
	
	class Meta:
		verbose_name = "Game"
		verbose_name_plural = "Games"


class GameImages(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="game_images/")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"GameImage {self.title}"
	
	class Meta:
		verbose_name = "Game Image"
		verbose_name_plural = "Game Images"


@receiver(post_delete, sender=Game)
def delete_game_files(instance, **kwargs):
	os.chdir("media/games")
	shutil.rmtree(instance.gamename)
	print("Файл игры успешно удалён!")
	os.chdir("../..")


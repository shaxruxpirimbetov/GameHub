from django.contrib.auth.models import User
from django.db import models
from games.models import Game


class PlayedGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Played Game by {self.user.username}"

    class Meta:
        verbose_name = "Played Game"
        verbose_name_plural = "Played Games"


class PageImage(models.Model):
	image = models.ImageField(upload_to="app_images/")

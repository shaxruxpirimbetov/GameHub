from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterApi.as_view()),
    path("played-game/", views.PlayedGameApi.as_view()),
    path("check-token/", views.CheckTokenApi.as_view()),
    path("page/", views.PageApi.as_view()),
    
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.GameApi.as_view()),
    
]
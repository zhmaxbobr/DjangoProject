from django.urls import path
from . import views


urlpatterns = [
    path("", views.index),
    path("anketa/",views.anketa, name="anketa"),
    path("profile/",views.view_profile,name="profile"),
    path("view_liked/", views.view_liked, name="liked"),
    path("view_disliked/", views.view_disliked, name="disliked")
]


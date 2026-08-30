from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("anketa/",views.anketa, name="anketa"),
    path("profile/",views.view_profile,name="profile"),
    path("view_liked/", views.view_liked, name="liked"),
    path("view_disliked/", views.view_disliked, name="disliked"),
    path("sign_up/",views.sign_up, name="sign_up"),
    path("match/",views.recomendation_search, name="match"),
    path("like/<int:user_id>",views.like, name="like"),
    path("dislike/<int:user_id>",views.dislike, name="dislike")
]


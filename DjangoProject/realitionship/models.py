from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name = "profile"
    )
    user_icon = models.ImageField(
        upload_to="icons/",
        blank=True,
        null=True,
        default="default_user_icon.jpg"
    )
    annotation = models.CharField(
        max_length=280,
        null=True
    )
    liked = models.ManyToManyField(User, related_name="liked", blank=True)
    disliked = models.ManyToManyField(User, related_name="disliked", blank=True)
    show_marked_items = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"Profile: {self.user.username}"

class Message(models.Model):
    text = models.CharField(
        max_length=4096,
        blank=False,
        null=False
    )
    sender_id = models.IntegerField()
    reciever_id = models.IntegerField()
    sent_at = models.DateTimeField(auto_now_add=True)

class Anketa(models.Model):
    GENDERS = [("female","Женского"), ("male","Мужского")]
    gender = models.CharField(choices=GENDERS, max_length=25)
    age = models.IntegerField()
    FIND_GENDERS = [("female","Женского"), ("male","Мужского"), ("both","Без разницы")]
    find_gender =  models.CharField(choices=FIND_GENDERS, max_length=25)
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE,related_name="anketa", null=True)

    def __str__(self):
        return f"Anketa: {self.profile.user.username}"

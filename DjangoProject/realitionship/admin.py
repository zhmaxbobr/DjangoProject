from django.contrib import admin
from .models import Anketa, Message, Profile
# Register your models here.

APP_MODELS = [Anketa,Message,Profile]
for model in APP_MODELS:
    admin.site.register(model)

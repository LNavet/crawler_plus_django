from os import name

from django.contrib import admin
from django.urls import path
from .views import ListMangas, update_content

urlpatterns = [
    path("", ListMangas.as_view(), name="list_all_mangas"),
    path("/update", update_content, name="update_list"),
]

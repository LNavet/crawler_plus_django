from django.shortcuts import render, HttpResponse
from jobs.tmo_scrapper import TMOScrapper
from .models import Manga
from django.views.generic import ListView

# Create your views here.
class ListMangas(ListView):
    model = Manga
    template_name = "mangas/list_mangas.html"
    context_object_name = "mangas"
    paginate_by = 24


def update_content(request):
    scraper = TMOScrapper()
    scraper.start_extraction()
    return HttpResponse("success")

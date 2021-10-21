from django.db import models
from django.db.models import UniqueConstraint


class Manga(models.Model):
    name = models.CharField(max_length=300, unique=True)
    uid = models.IntegerField(unique=True)
    cover = models.URLField(max_length=300)
    link_to_manga = models.URLField()

    def __str__(self):
        return self.name[:50]


class Chapter(models.Model):
    manga_id = models.ForeignKey("Manga", on_delete=models.CASCADE)
    uid = models.IntegerField()
    number = models.FloatField()
    cover = models.URLField(max_length=300)
    link_to_manga = models.URLField()

    class Meta:
        constraints = [
            UniqueConstraint(name="unique_chapters", fields=["uid", "number"])
        ]

    def __str__(self):
        return f"Chapter |{self.number}|"


class Update(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    chapters = models.ManyToManyField(Chapter)

    def __str__(self):
        return f"{self.created_at}"

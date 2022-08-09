from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateTimeField(default=0, null=True, blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='category', blank=True, null=True
    )
    description = models.TextField(max_length=1000, help_text='Краткое описание')
    rating = models.IntegerField(default=0, null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, related_name='genre', null=True)

    def __str__(self):
        return (
            'Заголовок {}, категория {}, жанр {}'.format(
                self.name, self.category, self.genre
            )
        )

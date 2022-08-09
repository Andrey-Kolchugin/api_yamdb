from django.contrib import admin

from .models import Title, Genre, Category


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year', 'rating', 'description',
        'category', 'genre'
    )
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre)
admin.site.register(Category)

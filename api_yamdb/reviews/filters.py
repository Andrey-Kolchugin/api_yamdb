from django_filters import rest_framework as df_filters

from .models import Title


class TitleFilter(df_filters.FilterSet):
    """Фильтр по полям произведений."""
    category = df_filters.CharFilter(field_name='category__slug',
                                     lookup_expr='icontains')
    genre = df_filters.CharFilter(field_name="genre__slug",
                                  lookup_expr='icontains')
    name = df_filters.CharFilter(field_name='name', lookup_expr='icontains')
    year = df_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')

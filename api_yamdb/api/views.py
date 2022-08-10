from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Title, Category, Genre
from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer, ReviewsSerializer, CommentSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]


class ReviewsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        review = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return post.comments.all()
    serializer_class = ReviewsSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]

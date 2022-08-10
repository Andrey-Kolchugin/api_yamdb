<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, CategoryViewSet, GenreViewSet, ReviewsViewSet
from . import views


v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews')
v1_router.register('users', views.AdminUserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', views.SignUp.as_view()),
    path('v1/auth/token/', views.ObtainToken.as_view()),
>>>>>>> origin/ivan
]

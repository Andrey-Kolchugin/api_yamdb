from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from reviews.models import Title, Category, Genre
from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer, ReviewsSerializer, CommentSerializer
from rest_framework import mixins
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.permissions import UserPermissions

from .serializers import (ObtainTokenSerializer, SafeUserSerializer,
                          SignUpSerializer, UserSerializer)

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




class SignUp(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(password='', confirmation_code='')

        username = request.data.get('username')
        email = request.data.get('email')
        user = get_object_or_404(User, username=username, email=email)

        confirmation_code = default_token_generator.make_token(user)

        user.password = confirmation_code
        user.confirmation_code = confirmation_code
        user.save()

        send_mail(
            'Код подтверждения',
            confirmation_code,
            from_email=None,
            recipient_list=[user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ObtainToken(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        serializer = ObtainTokenSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User,
            username=username,
        )

        if user.confirmation_code != confirmation_code:
            return Response(
                'Confirmation code is invalid',
                status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response(
            {'access_token': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, UserPermissions)
    lookup_field = 'username'
    PageNumberPagination.page_size = 10
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = SafeUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if kwargs['username'] != 'me':
            return super().destroy(request, *args, **kwargs)
        return Response(
            "You are not allowed to delete other's accounts",
            status=status.HTTP_403_FORBIDDEN
        )

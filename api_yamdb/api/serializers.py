from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import CurrentUserDefault
from reviews.models import Category, Genre, Title, User, Comment, Review
from users.models import User

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class TitleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        fields = '__all__'
        model = Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    """Регистрация пользователя."""

    class Meta:
        model = User
        fields = ('email', 'username')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя общего назначения."""

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name', 'bio', 'role')


class SafeUserSerializer(serializers.ModelSerializer):
    """Серилазиатор для пользователя с безопасными полями."""

    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        exclude = ('id', 'confirmation_code')


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('confirmation_code', 'username')

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if not username and not confirmation_code:
            raise serializers.ValidationError(
                f"Fields are blank {username}, {confirmation_code}"
            )
        return data

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError(
                "username can't be blank"
            )
        return value


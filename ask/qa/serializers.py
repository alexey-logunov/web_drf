from rest_framework import serializers
from .models import Question, Answer, UserQuestionRelation
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User
from taggit.models import Tag


class QuestionLikesSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class QuestionSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    # likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rate = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    author_name = serializers.CharField(source='author.username', default="", read_only=True)
    likes = QuestionLikesSerializers(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        # fields = ("id", "title", "text", "image", "slug", "added_at", "rating", "author", "likes", "tags")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    # def get_likes_count(self, instance):
    #     return UserQuestionRelation.objects.filter(question=instance, like=True).count()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("name",)
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class ContactSerailizer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    question = serializers.SlugRelatedField(slug_field="slug", queryset=Question.objects.all())

    class Meta:
        model = Answer
        # fields = '__all__'
        fields = ("question", "author", "text", "added_at")
        lookup_field = 'question'
        extra_kwargs = {
            'url': {'lookup_field': 'question'}
        }


class UserQuestionRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestionRelation
        fields = ('question', 'like', 'in_bookmarks', 'rate')




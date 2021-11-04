from rest_framework import serializers
from .models import Question
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User
from taggit.models import Tag


class QuestionSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Question
        fields = ("id", "title", "text", "image", "slug", "added_at", "rating", "author", "likes", "tags")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


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
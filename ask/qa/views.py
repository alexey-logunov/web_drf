from rest_framework import viewsets
from .serializers import QuestionSerializer
from .models import Question
from rest_framework.response import Response


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'slug'

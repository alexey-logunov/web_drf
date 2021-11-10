from django.db.models import Count, Case, When, Avg
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, pagination, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAuthorOrStaffOrReadOnly
from .serializers import QuestionSerializer, TagSerializer, ContactSerailizer, RegisterSerializer, UserSerializer, \
    AnswerSerializer, UserQuestionRelationSerializer
from .models import Question, Answer, UserQuestionRelation
from taggit.models import Tag
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    ordering = 'added_at'


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().annotate(
            annotated_likes=Count(Case(When(userquestionrelation__like=True, then=1))),
            rate=Avg('userquestionrelation__rate')).select_related('author').prefetch_related('likes').order_by('id')
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['author', 'added_at', 'rating']
    search_fields = ['title', 'text']
    ordering_fields = ['added_at', 'rating', 'author', 'likes']
    lookup_field = 'slug'
    permission_classes = [IsAuthorOrStaffOrReadOnly]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.AllowAny]

    # pagination_class = PageNumberSetPagination

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class TagDetailView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Question.objects.filter(tags=tag)


class AsideView(generics.ListAPIView):
    queryset = Question.objects.all().order_by('-id')[:3]
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    serializer_class = ContactSerailizer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerailizer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, from_email, ['al_logunov@mail.ru'])
            return Response({"success": "Sent"})


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })


class ProfileView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({
            "user": UserSerializer(request.user, context=self.get_serializer_context()).data,
        })


class AnswerView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        question_slug = self.kwargs['question_slug'].lower()
        question = Question.objects.get(slug=question_slug)
        return Answer.objects.filter(question=question)


def auth(request):
    return render(request, 'oauth.html')


class UserQuestionRelationView(UpdateModelMixin, GenericViewSet):
    queryset = UserQuestionRelation.objects.all()
    serializer_class = UserQuestionRelationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'question'

    def get_object(self):
        obj, _ = UserQuestionRelation.objects.get_or_create(user=self.request.user,
                                                            question_slug=self.kwargs['question'])
        return obj

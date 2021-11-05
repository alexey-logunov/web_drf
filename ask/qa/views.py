from rest_framework import viewsets, permissions, pagination, generics, filters
from .serializers import QuestionSerializer, TagSerializer, ContactSerailizer, RegisterSerializer, UserSerializer, \
    AnswerSerializer
from .models import Question, Answer
from taggit.models import Tag
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    ordering = 'added_at'


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ['author', 'added_at', 'rating']
    search_fields = ['title', 'text']
    ordering_fields = ['added_at', 'rating', 'author', 'likes']
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


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

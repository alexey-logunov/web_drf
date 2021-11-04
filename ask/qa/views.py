from rest_framework import viewsets, permissions, pagination, generics, filters
from .serializers import QuestionSerializer, TagSerializer, ContactSerailizer
from .models import Question
from taggit.models import Tag
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    ordering = 'added_at'


class QuestionViewSet(viewsets.ModelViewSet):
    search_fields = ['title', 'text']
    filter_backends = (filters.SearchFilter,)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class TagDetailView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]


    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Question.objects.filter(tags=tag)


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class AsideView(generics.ListAPIView):
    queryset = Question.objects.all().order_by('-id')[:3]
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerailizer

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
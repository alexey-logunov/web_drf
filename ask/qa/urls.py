from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, TagDetailView, TagView, AsideView, FeedBackView, RegisterView, ProfileView, \
    AnswerView

router = DefaultRouter()
router.register('questions', QuestionViewSet, basename='questions')

urlpatterns = [
    path("", include(router.urls)),
    path("tags/", TagView.as_view()),
    path("tags/<slug:tag_slug>/", TagDetailView.as_view()),
    path("aside/", AsideView.as_view()),
    path("feedback/", FeedBackView.as_view()),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path("answers/", AnswerView.as_view()),
    path("answers/<slug:question_slug>/", AnswerView.as_view()),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet

router = DefaultRouter()
router.register('question', QuestionViewSet, basename='question')

urlpatterns = [
    path("", include(router.urls))
]
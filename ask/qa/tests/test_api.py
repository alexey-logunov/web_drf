from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Question
from ..serializers import QuestionSerializer


class AskApiTestCase(APITestCase):
    def test_get(self):
        question_1 = Question.objects.create(title='Test question_1', text='Test question_1')
        question_2 = Question.objects.create(title='Test question_2', text='Test question_2')
        url = reverse('questions-list')
        response = self.client.get(url)
        serializer_data = QuestionSerializer([question_1, question_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


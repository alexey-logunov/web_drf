from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Question
from ..serializers import QuestionSerializer


class AskApiTestCase(APITestCase):

    def setUp(self):
        self.question_1 = Question.objects.create(title='title_question_1', text='text_question_1',
                                                  slug='slug1', rating=1)
        self.question_2 = Question.objects.create(title='title_question_2', text='text_question_2',
                                                  slug='slug2', rating=2)
        self.question_3 = Question.objects.create(title='title_question_3', text='title_question_1',
                                                  slug='slug3', rating=3)

    def test_get(self):
        url = reverse('questions-list')
        response = self.client.get(url)
        serializer_data = QuestionSerializer([self.question_1, self.question_2, self.question_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('questions-list')
        response = self.client.get(url, data={'rating': 2})
        serializer_data = QuestionSerializer([self.question_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('questions-list')
        response = self.client.get(url, data={'search': 'title_question_1'})
        serializer_data = QuestionSerializer([self.question_1, self.question_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

import json

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Question
from ..serializers import QuestionSerializer


class AskApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="test_username")
        self.question_1 = Question.objects.create(title="title_question_1", text="text_question_1",
                                                  slug="slug1", rating=1, author=self.user)
        self.question_2 = Question.objects.create(title="title_question_2", text="text_question_2",
                                                  slug="slug2", rating=2, author=self.user)
        self.question_3 = Question.objects.create(title="title_question_3", text="title_question_1",
                                                  slug="slug3", rating=3, author=self.user)

    def test_get(self):
        url = reverse("questions-list")
        response = self.client.get(url)
        serializer_data = QuestionSerializer([self.question_1, self.question_2, self.question_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse("questions-list")
        response = self.client.get(url, data={"rating": 3})
        serializer_data = QuestionSerializer([self.question_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    # def test_get_search(self):
    #     url = reverse("questions-list")
    #     response = self.client.get(url, data={"search": "title_question_1"})
    #     serializer_data = QuestionSerializer([self.question_1, self.question_3], many=True).data
    #     print(response.data)
    #     print(serializer_data)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, len(Question.objects.all()))
        url = reverse("questions-list")
        data = {
            "title": "Портрет потребителя: гипотеза и теории",
            "text": "<p>Такое понимание ситуации восходит к Эл Райс, при этом конкурент усиливает бизнес-план.</p>",
            "slug": "portrait-of-the-consumer",
            "rating": 1,
            "author": "test_username",
            "tags": ["consumer"]
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, len(Question.objects.all()))

    # def test_update(self):
    #     url = reverse("questions-detail", args=(self.question_1.id,))
    #     data = {
    #         "title": self.question_1.title,
    #         "text": self.question_1.text,
    #         "slug": self.question_1.slug,
    #         "rating": 2,
    #         "author": self.question_1.author,
    #         "tags": self.question_1.tags
    #     }
    #     json_data = json.dumps(data)
    #     self.client.force_login(self.user)
    #     response = self.client.put(url, data=json_data, content_type="application/json")
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.question_1.refresh_from_db()
    #     self.assertEqual(2, self.question_1.rating)
import json
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Question, UserQuestionRelation
from ..serializers import QuestionSerializer


class AskApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="test_username")
        self.question_1 = Question.objects.create(title="title_question_1", text="text_question_1",
                                                  slug="slug1", rating=1, author=self.user, tags=[])
        self.question_2 = Question.objects.create(title="title_question_2", text="text_question_2",
                                                  slug="slug2", rating=2, author=self.user, tags=[])
        self.question_3 = Question.objects.create(title="title_question_3", text="title_question_1",
                                                  slug="slug3", rating=3, author=self.user, tags=[])
        UserQuestionRelation.objects.create(user=self.user, question=self.question_1, like=True, rate=5)

    def test_get(self):
        url = reverse("questions-list")
        response = self.client.get(url)
        questions = Question.objects.all().annotate(
            annotated_likes=Count(Case(When(userquestionrelation__like=True, then=1))),
            rate=Avg('userquestionrelation__rate')).order_by('id')
        serializer_data = QuestionSerializer(questions, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['rate'], '5.00')
        self.assertEqual(serializer_data[0]['likes_count'], 1)
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)

    def test_get_filter(self):
        url = reverse("questions-list")
        questions = Question.objects.filter(id__in=[self.question_3.id]).annotate(
            annotated_likes=Count(Case(When(userquestionrelation__like=True, then=1))),
            rate=Avg('userquestionrelation__rate')).order_by('id')
        response = self.client.get(url, data={"rating": 3})
        serializer_data = QuestionSerializer(questions, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse("questions-list")
        questions = Question.objects.filter(id__in=[self.question_1.id, self.question_3.id]).annotate(
            annotated_likes=Count(Case(When(userquestionrelation__like=True, then=1))),
            rate=Avg('userquestionrelation__rate')).order_by('id')
        response = self.client.get(url, data={"q": "title_question_1"})
        serializer_data = QuestionSerializer(questions, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Question.objects.all().count())
        url = reverse("questions-list")
        data = {
            "title": "Портрет потребителя: гипотеза и теории",
            "text": "<p>Такое понимание ситуации восходит к Эл Райс, при этом конкурент усиливает бизнес-план.</p>",
            "slug": "portrait-of-the-consumer",
            "rating": 1,
            "author": self.user,
            "tags": ["consumer"]
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type="application/json")
        self.assertEqual(self.user, Question.objects.last().author)
        self.assertEqual(4, Question.objects.all().count())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)

    def test_update(self):
        url = reverse("questions-detail", args=(self.question_1.slug,))
        data = {
            "title": self.question_1.title,
            "text": self.question_1.text,
            "slug": self.question_1.slug,
            "rating": 2,
            # "author": "test_username",
            "tags": self.question_1.tags
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.question_1.refresh_from_db()
        self.assertEqual(2, self.question_1.rating)

    def test_update_not_author(self):
        self.user2 = User.objects.create(username="test_username2")
        url = reverse("questions-detail", args=(self.question_1.slug,))
        data = {
            "title": self.question_1.title,
            "text": self.question_1.text,
            "slug": self.question_1.slug,
            "rating": 2,
            "author": "test_username",
            "tags": self.question_1.tags
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, response.data)
        self.question_1.refresh_from_db()
        self.assertEqual(1, self.question_1.rating)

    def test_update_not_author_but_staff(self):
        self.user2 = User.objects.create(username="test_username2", is_staff=True)
        url = reverse("questions-detail", args=(self.question_1.slug,))
        data = {
            "title": self.question_1.title,
            "text": self.question_1.text,
            "slug": self.question_1.slug,
            "rating": 2,
            "tags": self.question_1.tags
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.question_1.refresh_from_db()
        self.assertEqual(2, self.question_1.rating)


class AskRelationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="test_username")
        self.user2 = User.objects.create(username="test_username2")
        self.question_1 = Question.objects.create(title="title_question_1", text="text_question_1",
                                                  slug="slug1", rating=1, author=self.user, tags=[])
        self.question_2 = Question.objects.create(title="title_question_2", text="text_question_2",
                                                  slug="slug2", rating=2, author=self.user, tags=[])

    def test_like(self):
        url = reverse("userquestionrelation-detail", args=(self.question_1.slug,))
        data = {
            "like": True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        relation = UserQuestionRelation.objects.get(user=self.user, question=self.question_1)
        self.assertTrue(relation.like)
        data = {
            "in_bookmarks": True
        }
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        relation = UserQuestionRelation.objects.get(user=self.user, question=self.question_1)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        url = reverse("userquestionrelation-detail", args=(self.question_1.slug,))
        data = {
            "rate": 3
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        relation = UserQuestionRelation.objects.get(user=self.user, question=self.question_1)
        self.assertEqual(3, relation.rate)

    def test_rate_wrong(self):
        url = reverse("userquestionrelation-detail", args=(self.question_1.slug,))
        data = {
            "rate": 6
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)

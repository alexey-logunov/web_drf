from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Question
from ..serializers import QuestionSerializer


class QuestionSerializerTestCase(TestCase):
    def test_ok(self):
        self.user = User.objects.create(username="test_username")
        self.question_1 = Question.objects.create(title="title_question_1", text="text_question_1",
                                                  slug="slug1", rating=1, author=self.user, tags=["tag1"])
        self.question_2 = Question.objects.create(title="title_question_2", text="text_question_2",
                                                  slug="slug2", rating=2, author=self.user, tags=["tag2"])
        data = QuestionSerializer([self.question_1, self.question_2], many=True).data
        expected_data = [
            {
                    "id": 1,
                    "tags": ["tag1"],
                    "author": "test_username",
                    "title": "title_question_1",
                    "text": "text_question_1",
                    "image": None,
                    "slug": "slug1",
                    "added_at": "2021-11-08",
                    "rating": 1,
                    "likes": []
            },
            {
                "id": 2,
                "tags": ["tag2"],
                "author": "test_username",
                "title": "title_question_2",
                "text": "text_question_2",
                "image": None,
                "slug": "slug2",
                "added_at": "2021-11-08",
                "rating": 2,
                "likes": []
            }
        ]
        self.assertEqual(expected_data, data)

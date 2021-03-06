from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from ..models import Question, UserQuestionRelation
from ..serializers import QuestionSerializer


class QuestionSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username="user1", first_name="Ivan", last_name='Ivanov')
        user2 = User.objects.create(username="user2", first_name="Semen", last_name='Semenov')
        user3 = User.objects.create(username="user3", first_name="Vasily", last_name='Pupkin')
        question_1 = Question.objects.create(title="title_question_1", text="text_question_1",
                                             slug="slug1", rating=1, tags=["tag1"], author=user1)
        question_2 = Question.objects.create(title="title_question_2", text="text_question_2",
                                             slug="slug2", rating=2, tags=["tag2"])
        UserQuestionRelation.objects.create(user=user1, question=question_1, like=True, rate=5)
        UserQuestionRelation.objects.create(user=user2, question=question_1, like=True, rate=5)
        user_question_3 = UserQuestionRelation.objects.create(user=user3, question=question_1, like=True)
        user_question_3.rate = 4
        user_question_3.save()

        UserQuestionRelation.objects.create(user=user1, question=question_2, like=True, rate=3)
        UserQuestionRelation.objects.create(user=user2, question=question_2, like=True, rate=4)
        UserQuestionRelation.objects.create(user=user3, question=question_2, like=False)

        questions = Question.objects.all().annotate(
            annotated_likes=Count(Case(When(userquestionrelation__like=True, then=1))),
            rate=Avg('userquestionrelation__rate')).order_by('id')

        data = QuestionSerializer(questions, many=True).data
        expected_data = [
            {
                "id": question_1.id,
                "tags": ["tag1"],
                "author_name": "user1",
                "title": "title_question_1",
                "text": "text_question_1",
                "image": None,
                "slug": "slug1",
                "added_at": "2021-11-09",
                "rating": 1,
                "likes": [
                    {
                        "first_name": "Ivan",
                        "last_name": "Ivanov"
                    },
                    {
                        "first_name": "Semen",
                        "last_name": "Semenov"
                    },
                    {
                        "first_name": "Vasily",
                        "last_name": "Pupkin"
                    }
                ],
                # "likes_count": 3,
                "annotated_likes": 3,
                "rate": '4.67'
            },
            {
                "id": question_2.id,
                "tags": ["tag2"],
                "author_name": "",
                "title": "title_question_2",
                "text": "text_question_2",
                "image": None,
                "slug": "slug2",
                "added_at": "2021-11-09",
                "rating": 2,
                "likes": [
                    {
                        "first_name": "Ivan",
                        "last_name": "Ivanov"
                    },
                    {
                        "first_name": "Semen",
                        "last_name": "Semenov"
                    },
                    {
                        "first_name": "Vasily",
                        "last_name": "Pupkin"
                    }
                ],
                # "likes_count": 2,
                "annotated_likes": 2,
                "rate": '3.5'
            }
        ]
        self.assertEqual(expected_data, data)

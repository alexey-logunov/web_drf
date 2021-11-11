from django.contrib.auth.models import User
from django.test import TestCase

from qa.logic import set_rating
from qa.models import Question, UserQuestionRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1", first_name="Ivan", last_name='Ivanov')
        user2 = User.objects.create(username="user2", first_name="Semen", last_name='Semenov')
        user3 = User.objects.create(username="user3", first_name="Vasily", last_name='Pupkin')
        self.question_1 = Question.objects.create(title="title_question_1", text="text_question_1",
                                             slug="slug1", rating=1, tags=["tag1"], author=user1)

        UserQuestionRelation.objects.create(user=user1, question=self.question_1, like=True, rate=5)
        UserQuestionRelation.objects.create(user=user2, question=self.question_1, like=True, rate=5)
        UserQuestionRelation.objects.create(user=user3, question=self.question_1, like=True, rate=4)


    def test_ok(self):
        set_rating(self.question_1)
        self.question_1.refresh_from_db()
        self.assertEqual('4.67', str(self.question_1.rating))

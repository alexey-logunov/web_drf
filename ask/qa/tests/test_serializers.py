from django.test import TestCase

from ..models import Question
from ..serializers import QuestionSerializer


class QuestionSerializerTestCase(TestCase):
    def test_ok(self):
        question_1 = Question.objects.create(title='Test question_1', text='Test question_1')
        question_2 = Question.objects.create(title='Test question_2', text='Test question_2')
        data = QuestionSerializer([question_1, question_2], many=True).data
        expected_data = [
            {
                'id': question_1.id,
                'title': 'Test question_1',
                'text': 'Test question_1'
            },
            {
                'id': question_2.id,
                'title': 'Test question_2',
                'text': 'Test question_2'
            }
        ]
        self.assertEqual(expected_data, data)

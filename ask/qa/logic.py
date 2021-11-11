from django.db.models import Avg

from qa.models import UserQuestionRelation


def set_rating(question):
    rating = UserQuestionRelation.objects.filter(question=question).aggregate(rating=Avg('rate')).get('rating')
    question.rating = rating
    question.save()

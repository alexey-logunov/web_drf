from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


# from ckeditor_uploader.fields import RichTextUploadingField
# from django.conf import settings
# from django.utils import timezone


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название вопроса')
    text = models.TextField(verbose_name='Описание вопроса')
    image = models.ImageField(blank=True, verbose_name='Картинка')
    slug = models.SlugField()
    added_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации вопроса')  # default=timezone.now
    rating = models.IntegerField(default=0, verbose_name='Рейтинг вопроса')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_question',
                               verbose_name='Автор вопроса')
    likes = models.ManyToManyField(User, blank=True, related_name='likes_set', verbose_name='Кому понравился вопрос')
    # likes_q = models.ManyToManyField(User, through='UserQuestionRelation')
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-added_at']

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_name',
                               verbose_name='Автор ответа')
    text = models.TextField(verbose_name='Текст ответа')
    added_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации ответа')  # default=timezone.now

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return self.text


class UserQuestionRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    like = models.BooleanField(default=False, verbose_name='Лайк')
    in_bookmarks = models.BooleanField(default=False, verbose_name='Закладки')
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True, verbose_name='Оценка')

    class Meta:
        verbose_name = 'Отношение'
        verbose_name_plural = 'Отношения'

    def __str__(self):
        return f'{self.user.username}: {self.question.title}, оценка: {self.rate}'

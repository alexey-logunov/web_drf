from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255, blank=True, verbose_name='Название вопроса')
    text = RichTextUploadingField(blank=True, verbose_name='Описание вопроса')
    image = models.ImageField(blank=True, verbose_name='Картинка')
    slug = models.SlugField(blank=True)
    added_at = models.DateField(default=timezone.now, verbose_name='Дата публикации вопроса')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг вопроса')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор вопроса')
    likes = models.ManyToManyField(User, related_name='likes_set', verbose_name='Количество лайков вопроса')
    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-added_at']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name', verbose_name='Автор ответа')
    text = models.TextField(blank=True, verbose_name='Текст ответа')
    added_at = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации ответа')

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return self.text

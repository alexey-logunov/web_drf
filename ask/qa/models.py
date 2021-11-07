from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
# from django.conf import settings
# from django.utils import timezone


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название вопроса')
    text = RichTextUploadingField(verbose_name='Описание вопроса')
    image = models.ImageField(blank=True, verbose_name='Картинка')
    slug = models.SlugField()
    added_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации вопроса')  # default=timezone.now
    rating = models.IntegerField(default=0, verbose_name='Рейтинг вопроса')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор вопроса')
    likes = models.ManyToManyField(User, blank=True, related_name='likes_set', verbose_name='Количество лайков вопроса')
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-added_at']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name', verbose_name='Автор ответа')
    text = models.TextField(verbose_name='Текст ответа')
    added_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации ответа')  # default=timezone.now

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return self.text

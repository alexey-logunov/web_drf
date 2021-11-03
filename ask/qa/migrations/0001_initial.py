# Generated by Django 3.2.9 on 2021-11-03 18:45

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Название вопроса')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Описание вопроса')),
                ('image', models.ImageField(upload_to='')),
                ('added_at', models.DateField(default=django.utils.timezone.now, verbose_name='Дата публикации вопроса')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг вопроса')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор вопроса')),
                ('likes', models.ManyToManyField(related_name='likes_set', to=settings.AUTH_USER_MODEL, verbose_name='Количество лайков вопроса')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ['-added_at'],
            },
        ),
    ]

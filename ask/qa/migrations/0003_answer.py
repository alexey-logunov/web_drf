
# Generated by Django 3.2.9 on 2021-11-04 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qa', '0002_auto_20211103_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='Текст ответа')),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публикации ответа')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_name', to=settings.AUTH_USER_MODEL, verbose_name='Автор ответа')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='qa.question', verbose_name='Вопрос')),
            ],
            options={
                'ordering': ['-added_at'],
            },
        ),
    ]
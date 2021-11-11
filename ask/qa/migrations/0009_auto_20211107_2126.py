# Generated by Django 3.2.9 on 2021-11-07 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0008_alter_question_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='added_at',
            field=models.DateField(auto_now_add=True, verbose_name='Дата публикации ответа'),
        ),
        migrations.AlterField(
            model_name='question',
            name='added_at',
            field=models.DateField(auto_now_add=True, verbose_name='Дата публикации вопроса'),
        ),
    ]
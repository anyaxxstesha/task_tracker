from datetime import timedelta

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Task(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название задачи',
        help_text='Укажите название задачи',
    )
    description = models.TextField(
        verbose_name='Текст задачи',
        help_text='Добавьте текст задачи',
        **NULLABLE
    )
    image = models.ImageField(
        upload_to='tasks/images',
        verbose_name='Изображение',
        help_text='Загрузите изображение для задачи, если это необходимо',
        **NULLABLE
    )
    file = models.FileField(
        upload_to='tasks/files',
        verbose_name='Файл',
        help_text='Загрузите файл для задачи, если это необходимо',
        **NULLABLE
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Флаг публичной/приватной задачи',
        help_text='Укажите, будет ли задача публичной'
    )
    presumable_completion_time = models.DurationField(
        default=timedelta(hours=5),
        verbose_name='Предполагаемое время выполнения',
        help_text='Укажите предполагаемое время выполнения задачи',
        **NULLABLE
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title

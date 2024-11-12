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
        upload_to='blog/images',
        verbose_name='Изображение',
        help_text='Загрузите изображение для задачи, если это необходимо',
        **NULLABLE
    )
    file = models.FileField(
        upload_to='blog/files',
        verbose_name='Файл',
        help_text='Загрузите файл для задачи, если это необходимо',
        **NULLABLE
    )
    views_amount = models.PositiveIntegerField(
        default=0,
        verbose_name='Просмотры',
        help_text='Счетчик просмотров задачи'
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title

from datetime import timedelta

from django.db import models

from users.models import User

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


class StatusTypeChoices(models.TextChoices):
    """Status type choices"""
    CREATED = 'Задача создана'
    ASSIGNED = 'Назначен исполнитель'
    COMPLETED = 'Задача выполнена'
    REVIEWED = 'Задача проверена'


class Status(models.Model):
    """Status database model"""
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='statuses'
    )
    type = models.CharField(
        max_length=20,
        choices=StatusTypeChoices,
        verbose_name='Тип статуса'
    )
    person_in_charge = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='statuses',
        verbose_name='Ответственное лицо',
        **NULLABLE
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания статуса',
    )

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        constraints = (models.UniqueConstraint(fields=['task', 'type'], name='task_type_unique_constraint'),)

    def __str__(self):
        return f'{self.type} - {self.task.title}'

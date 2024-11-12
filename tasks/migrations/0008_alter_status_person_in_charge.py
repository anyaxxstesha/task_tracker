# Generated by Django 5.1.3 on 2024-11-12 21:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_status_created_at_alter_status_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='person_in_charge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='statuses', to=settings.AUTH_USER_MODEL, verbose_name='Ответственное лицо'),
        ),
    ]

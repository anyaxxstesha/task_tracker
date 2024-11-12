from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'views_amount', 'presumable_completion_time', 'is_public')
    list_filter = ('title',)
    search_fields = ('title', 'description')

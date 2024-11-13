from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'presumable_completion_time')
    list_filter = ('title',)
    search_fields = ('title', 'description')

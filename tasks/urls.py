from django.urls import path

from tasks.apps import TasksConfig
from tasks.views import TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, StatusCreateView, \
    StatusUpdateView

app_name = TasksConfig.name

urlpatterns = [
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('', TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),

    path('tasks/<int:task_pk>/status/create/', StatusCreateView.as_view(), name='status_create'),
    path('tasks/status/<int:pk>/update/', StatusUpdateView.as_view(), name='status_update')
]

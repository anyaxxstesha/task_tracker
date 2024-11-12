from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from tasks.models import Task


class TaskListView(ListView):
    model = Task


class TaskDetailView(DetailView):
    model = Task

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_amount += 1
        self.object.save()
        return self.object


class TaskCreateView(CreateView):
    model = Task
    fields = ('title', 'description', 'image', 'file')
    success_url = reverse_lazy('tasks:task_list')


class TaskUpdateView(UpdateView):
    model = Task
    fields = ('title', 'description', 'image', 'file')

    def get_success_url(self):
        return reverse('tasks:task_detail', kwargs={'pk': self.object.pk})


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from tasks.forms import StatusForm
from tasks.models import Task, Status, StatusTypeChoices


class TaskListView(LoginRequiredMixin, ListView):
    model = Task

    def get_queryset(self):
        return self.model.objects.prefetch_related('statuses').all()


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    def get_queryset(self):
        return self.model.objects.prefetch_related('statuses').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statuses = self.object.statuses.order_by('created_at').all()
        context['forms'] =  [StatusForm(instance=status) for status in statuses]
        context['types'] = StatusTypeChoices
        if len(statuses) < 4:
            context['empty_form'] = StatusForm()
            last = context['forms'][-1].instance
            if last.type == StatusTypeChoices.CREATED:
                context['empty_form_title'] = 'Назначить исполнителя'
            elif last.type == StatusTypeChoices.ASSIGNED:
                context['empty_form_title'] = 'Подтвердить выполнение'
            elif last.type == StatusTypeChoices.COMPLETED:
                context['empty_form_title'] = 'Одобрить решение'
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ('title', 'description', 'image', 'file')
    success_url = reverse_lazy('tasks:task_list')
    def form_valid(self, form):
        self.object = form.save()
        Status.objects.create(task=self.object, type=StatusTypeChoices.CREATED, person_in_charge=self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ('title', 'description', 'image', 'file')

    def get_success_url(self):
        return reverse('tasks:task_detail', kwargs={'pk': self.object.pk})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm

    def get_success_url(self):
        return reverse('tasks:task_detail', kwargs={'pk': self.object.task.pk})

    def form_valid(self, form):
        task_pk = self.kwargs.get('task_pk', '')
        try:
            task = Task.objects.get(pk=task_pk)
        except Task.DoesNotExists:
            raise Http404
        self.object = form.save(commit=False)
        self.object.task = task
        newest_status = task.statuses.order_by('created_at').last()
        if newest_status.type == StatusTypeChoices.CREATED:
            self.object.type = StatusTypeChoices.ASSIGNED
        elif newest_status.type == StatusTypeChoices.ASSIGNED:
            self.object.type = StatusTypeChoices.COMPLETED
        else:
            self.object.type = StatusTypeChoices.REVIEWED
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm

    def get_success_url(self):
        return reverse('tasks:task_detail', kwargs={'pk': self.object.task.pk})

import secrets

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, FormView, ListView, DetailView, UpdateView, DeleteView

from users.forms import UserRegisterForm, UserResetForm, UserForm
from users.models import User
from users.services import send_verification_mail


class UserCreateView(CreateView):
    """
    View for registering new users.
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = secrets.token_hex(16)
        user.token = token
        host = settings.MAIN_HOST
        send_verification_mail(host, user.email, token)
        return super().form_valid(form)


class EmailVerification(View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, token=self.kwargs.get('token', ''))
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('users:login'))


class UserResetView(FormView):
    form_class = UserResetForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.user
        password = self.generate_password()
        user.password = make_password(password)
        user.save()

        send_mail(
            subject='Сброс пароля',
            message=f'Ваш новый пароль: {password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

    @staticmethod
    def generate_password():
        return secrets.token_hex(5)


class UserListView(ListView):
    model = User


class UserDetailView(DetailView):
    model = User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm

    def get_success_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.object.pk})


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:user_list')

import secrets

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, FormView

from users.forms import UserRegisterForm, UserResetForm
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
        host = self.request.get_host()
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

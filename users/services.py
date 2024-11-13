from django.conf import settings
from django.core.mail import send_mail


def send_verification_mail(host, email, token):
    """Sends a verification email"""
    url = f'{host}/users/email-confirm/{token}'
    send_mail(
        subject='Подтверждение почты',
        message=f'Для подтверждения вашей почты перейдите по ссылке: {url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

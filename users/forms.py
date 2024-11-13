from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, EmailField, ValidationError, BooleanField, ModelForm

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserResetForm(StyleFormMixin, Form):
    email = EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if not qs.exists():
            raise ValidationError('Пользователь с таким email не найден')
        self.user = qs.first()
        return email

class UserForm(StyleFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ('name', 'lastname', 'avatar', 'country', 'phone')

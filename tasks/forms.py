from django.forms import ModelForm, forms, BooleanField, IntegerField

from tasks.models import Task, Status


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class TaskForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'image', 'file', 'presumable_completion_time', 'is_public')

    @staticmethod
    def check_restrictions(field, field_name):
        restrictions = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                        'бесплатно', 'обман', 'полиция', 'радар']  # Запрещенные слова
        for word in restrictions:
            if word in field:
                raise forms.ValidationError(f"В поле {field_name} присутствует запрещенное слово: {word}")

    def clean_title(self):
        name = self.cleaned_data.get('title')
        self.check_restrictions(name, 'title')

        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        self.check_restrictions(description, 'description')

        return description


class StatusForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Status
        fields = ('person_in_charge',)

from .models import Courses
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea


class CoursesForm(ModelForm):
    class Meta:
        model = Courses
        fields = ['title', 'description', 'date']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название курса'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание курса'
            }),
            "date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата публикации'
            }),
        }
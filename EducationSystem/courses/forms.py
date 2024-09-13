from .models import Courses, Modules, Lessons, Assignment, Enrollment
from django.forms import ModelForm, TextInput, DateInput, Textarea


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
            "date": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата публикации',
                'type': 'date'
            }),
        }


class ModuleForm(ModelForm):
    class Meta:
        model = Modules
        fields = ['title', 'description']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название модуля'
            }),
        }


class LessonForm(ModelForm):
    class Meta:
        model = Lessons
        fields = ['title', 'content']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название урока'
            }),
            'content': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Содержание урока'
            }),
        }


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название задания'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание задания'
            }),
        }

#Запись на курсы
class EnrollmentForm(ModelForm):
    class Meta:
        model = Enrollment
        fields = []


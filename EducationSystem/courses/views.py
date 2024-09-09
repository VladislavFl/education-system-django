from django.shortcuts import render, redirect
from .models import Courses
from .forms import CoursesForm

def courses_home(request):
    courses = Courses.objects.all()
    return render(request, 'courses/courses_home.html', { 'courses': courses })


def create(request):
    error = ''
    if request.method == 'POST':
        form = CoursesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма не верная'

    form = CoursesForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'courses/create.html', data)

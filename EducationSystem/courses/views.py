from django.shortcuts import render, redirect
from .models import Courses,Modules,Lessons,Assignment
from .forms import CoursesForm,ModuleForm,LessonForm,AssignmentForm

def courses_home(request):
    courses = Courses.objects.all()
    return render(request, 'courses/courses_home.html', { 'courses': courses })


def create_course(request):
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
    return render(request, 'courses/create_course.html', data)

def create_module(request, course_id):
    course = Courses.objects.get(id=course_id)
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            return redirect('create_lesson', module_id=module.id)
    else:
        form = ModuleForm()
    return render(request, 'courses/create_module.html', {'form': form, 'course': course})

def create_lesson(request, module_id):
    module = Modules.objects.get(id=module_id)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            return redirect('create_assignment', lesson_id=lesson.id)
    else:
        form = LessonForm()
    return render(request, 'courses/create_lesson.html', {'form': form, 'module': module})

def create_assignment(request, lesson_id):
    lesson = Lessons.objects.get(id=lesson_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.lesson = lesson
            assignment.save()
            return redirect('courses_home')
    else:
        form = AssignmentForm()
    return render(request, 'courses/create_assignment.html', {'form': form, 'lesson': lesson})

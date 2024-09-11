from django.shortcuts import render, redirect, get_object_or_404
from .models import Courses,Modules,Lessons,Assignment,Enrollment
from .forms import CoursesForm,ModuleForm,LessonForm,AssignmentForm
from django.contrib.auth.decorators import login_required

def courses_home(request):
    courses = Courses.objects.all()
    return render(request, 'courses/courses_home.html', { 'courses': courses })


def create_course(request):
    error = ''
    if request.method == 'POST':
        form = CoursesForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('create_module', course_id=course.id)
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

def course_detail(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    modules = course.modules.all()
    #lessons = course.lessons.all()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'lessons': 3,
    })





@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        if created:
            return redirect('courses:course_detail', course_id=course.id)  # Переход к деталям курса
        else:
            return render(request, 'courses/enrollment_error.html', {'course': course})

    return render(request, 'courses/enroll_in_course.html', {'course': course})

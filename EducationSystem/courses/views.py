from datetime import timezone

from django.shortcuts import render, redirect, get_object_or_404
from .models import Courses, Modules, Lessons, Assignment, Enrollment
from .forms import CoursesForm, ModuleForm, LessonForm, AssignmentForm, EnrollmentForm
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


# Функция для просмотра уроков
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    assignments = lesson.assignments.all()
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson, 'assignments': assignments})

# Функция для записи на курс
@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

    if created:
        message = "Вы успешно записались на курс!"
    else:
        message = "Вы уже записаны на этот курс."

    return render(request, 'courses/enrollment_success.html', {'message': message, 'course': course})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    if request.method == 'POST':
        form = CoursesForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses_home')
    else:
        form = CoursesForm(instance=course)
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})

@login_required
def edit_module(request, module_id):
    module = get_object_or_404(Modules, id=module_id)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('create_lesson', module_id=module.id)
    else:
        form = ModuleForm(instance=module)
    return render(request, 'courses/edit_module.html', {'form': form, 'module': module})

@login_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('create_assignment', lesson_id=lesson.id)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'courses/edit_lesson.html', {'form': form, 'lesson': lesson})

@login_required
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('courses_home')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'courses/edit_assignment.html', {'form': form, 'assignment': assignment})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('courses_home')
    return render(request, 'courses/delete_course.html', {'course': course})

@login_required
def delete_module(request, module_id):
    module = get_object_or_404(Modules, id=module_id)
    if request.method == 'POST':
        module.delete()
        return redirect('courses_home')
    return render(request, 'courses/delete_module.html', {'module': module})

@login_required
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    if request.method == 'POST':
        lesson.delete()
        return redirect('courses_home')
    return render(request, 'courses/delete_lesson.html', {'lesson': lesson})

@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        assignment.delete()
        return redirect('courses_home')
    return render(request, 'courses/delete_assignment.html', {'assignment': assignment})
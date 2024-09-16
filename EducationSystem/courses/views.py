from datetime import timezone
import random
from sys import modules

from django.shortcuts import render, redirect, get_object_or_404
from .models import Courses, Modules, Lessons, Assignment, Enrollment
from .forms import CoursesForm, ModuleForm, LessonForm, AssignmentForm, EnrollmentForm
from django.contrib.auth.decorators import login_required

def courses_home(request):
    courses = Courses.objects.all()
    image_urls = [
        "https://cms-b-assets.familysearch.org/dims4/default/34288f5/2147483647/strip/true/crop/900x601+0+0/resize/2400x1602!/format/jpg/quality/90/?url=https%3A%2F%2Ffamilysearch-brightspot.s3.amazonaws.com%2Fea%2Ffe%2Fe29f2f4a76961ad52ef55aaeecc8%2Fadobestock-106776715.jpg",
        "https://www.asb-hamburg.de/fileadmin/_processed_/a/d/csm_Generation_60plus_Freiwilligaktiv_AdobeStock_57522810_742a6441bd.jpeg",
        "https://avatars.mds.yandex.net/i?id=ddeccd76690f6ec52743365e147019dc_l-4265706-images-thumbs&n=13",
        "https://avatars.mds.yandex.net/i?id=b8def118b2774d5ef5a3f493fdd36a29_l-10814666-images-thumbs&n=13",
        "https://cdn.culture.ru/images/165efd63-61b7-5f91-961c-ab7190104023",
        "https://cdn.culture.ru/images/7e9c1e77-ba1b-5bc0-b214-edd31b8dfc8a",
        "https://avatars.mds.yandex.net/i?id=3b40090ba5910481b8e55104c3e583e3_l-5478197-images-thumbs&n=13",
        "https://lenobl.ru/media/news/images/2020/01/22/b793dfb3-adbd-495b-8ade-9c57747426a2.jpg",
    ]

    for course in courses:
        course.random_image = random.choice(image_urls)
    return render(request, 'courses/courses_home.html', { 'courses': courses })


def create_course(request):
    error = ''
    if request.method == 'POST':
        form = CoursesForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', course_id=course.id)
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
            return redirect('module_detail', module_id=module.id)# Перенаправляем на страницу модуля
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
            return redirect('lesson_detail', lesson_id=lesson.id)
    else:
        form = AssignmentForm()
    return render(request, 'courses/create_assignment.html', {'form': form, 'lesson': lesson})

def course_detail(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    modules = course.modules.all()
    if request.method == 'POST':
        # Здесь можно добавить логику для обработки сохранения курса
        course.save()  # Сохраняем курс, если это необходимо
        return redirect('course_detail', course_id=course.id)  # Перенаправляем на страницу курса

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'lessons': 3,
    })

def module_detail(request, module_id):
    module = get_object_or_404(Modules, id=module_id)
    lessons = module.lessons.all()  # Получаем все уроки модуля
    course = module.course  # Получаем курс, к которому принадлежит модуль
    return render(request, 'courses/module_detail.html', {
        'module': module,
        'lessons': lessons,
        'course': course,  # Передаем курс в контекст
    })

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    module = lesson.module  # Получаем модуль из урока
    if module is None:
        # Обработка случая, если модуль не найден
        return render(request, 'courses/error.html', {'message': 'Модуль не найден.'})

    course = module.course  # Получаем курс из модуля

    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        return redirect('access_denied', course_id=course.id)

    assignments = lesson.assignments.all()
    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'assignments': assignments,
        'module': module,  # Передаем модуль в контекст
    })

def assignment_detail(request, assignment_id):
    # Получаем задание по его идентификатору
    assignment = get_object_or_404(Assignment, id=assignment_id)
    lesson = assignment.lesson  # Предполагается, что задание связано с уроком

    # Отправляем данные в шаблон
    return render(request, 'courses/assignment_detail.html', {
        'assignment': assignment,
        'lesson': lesson,
    })
def access_denied(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    return render(request, 'courses/access_denied.html', {'course': course})

# Функция для записи на курс
@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

    if created:
        message = "Вы успешно записались на курс!"
        # Получаем первую лекцию из модуля курса
        first_module = course.modules.first()
        if first_module:
            first_lesson = first_module.lessons.first()
            if first_lesson:
                return redirect('lesson_detail', lesson_id=first_lesson.id)
    else:
        message = "Вы уже записаны на этот курс."

    return render(request, 'courses/enrollment_success.html', {'message': message, 'course': course})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    if request.method == 'POST':
        form = CoursesForm(request.POST, instance=course)
        if form.is_valid():
            form.save()# Сохраняем изменения
            return redirect('course_detail', course_id=course.id)  # Перенаправляем на страницу курса
    else:
        form = CoursesForm(instance=course)
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('courses_home')
    return render(request, 'courses/delete_course.html', {'course': course})

@login_required
def edit_module(request, module_id):
    module = get_object_or_404(Modules, id=module_id)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('module_detail', module_id=module.id)# Перенаправляем на страницу модуля
    else:
        form = ModuleForm(instance=module)
    return render(request, 'courses/edit_module.html', {'form': form, 'module': module})

@login_required
def delete_module(request, module_id):
    # Получаем модуль или выдаем 404, если не найден
    module = get_object_or_404(Modules, id=module_id)
    course_id = module.course.id  # Сохраняем ID курса для перенаправления

    if request.method == 'POST':
        module.delete()  # Удаляем модуль
        return redirect('course_detail', course_id=course_id)  # Перенаправляем к деталям курса

    return render(request, 'courses/delete_module.html', {'module': module}) # Возвращаем страницу подтверждения удаления модуля

@login_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lesson_detail', lesson_id=lesson.id)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'courses/edit_lesson.html', {'form': form, 'lesson': lesson})

@login_required
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    module_id = lesson.module.id  # Получаем ID модуля, к которому принадлежит урок
    if request.method == 'POST':
        lesson.delete()  # Удаляем урок
        return redirect('module_detail', module_id=module_id)  # Перенаправляем к деталям модуля
    return render(request, 'courses/delete_lesson.html', {'lesson': lesson})

@login_required
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_detail', assignment_id=assignment_id)
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'courses/edit_assignment.html', {'form': form, 'assignment': assignment})


@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    lesson_id = assignment.lesson.id
    if request.method == 'POST':
        assignment.delete()
        return redirect('lesson_detail', lesson_id=lesson_id)
    return render(request, 'courses/delete_assignment.html', {'assignment': assignment})


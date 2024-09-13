from django.urls import path
from . import views

urlpatterns = [
    path('', views.courses_home, name='courses_home'),
    path('create_course', views.create_course, name='create_course'),
    path('create_module/<int:course_id>/', views.create_module, name='create_module'),
    path('create_lesson/<int:module_id>/', views.create_lesson, name='create_lesson'),
    path('create_assignment/<int:lesson_id>/', views.create_assignment, name='create_assignment'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),# Просмотр деталей курса
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),  # Просмотр деталей урока
    path('module/<int:module_id>/', views.module_detail, name='module_detail'),# Детали модуля
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),# Детали урока
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),  # Запись на курс
    path('access_denied/<int:course_id>/', views.access_denied, name='access_denied'),
    path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),# Редактирование курса
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),# Удаление курса
    path('edit_module/<int:module_id>/', views.edit_module, name='edit_module'),# Редактирование модуля
    path('delete_module/<int:module_id>/', views.delete_module, name='delete_module'),# Удаление модуля
    path('edit_lesson/<int:lesson_id>/', views.edit_lesson, name='edit_lesson'),# Редактирование урока
    path('delete_lesson/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),# Удаление урока
    path('edit_assignment/<int:assignment_id>/', views.edit_assignment, name='edit_assignment'),# Редактирование задания
    path('delete_assignment/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),# Удаление задания

    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    ]



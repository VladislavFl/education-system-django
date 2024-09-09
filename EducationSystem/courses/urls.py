from django.urls import path
from . import views

urlpatterns = [
    path('', views.courses_home, name='courses_home'),
    path('create_course', views.create_course, name='create_course'),
    path('create_module/<int:course_id>/', views.create_module, name='create_module'),
    path('create_lesson/<int:module_id>/', views.create_lesson, name='create_lesson'),
    path('create_assignment/<int:lesson_id>/', views.create_assignment, name='create_assignment'),
]

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html',
                                                authentication_form=UserLoginForm),
                                                name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('teacher_profile/', views.teacher_profile, name='teacher_profile'),
    path('profile/', views.teacher_profile, name='profile'),

]
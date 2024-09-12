from django.db import models
from django.contrib.auth.models import User

class Courses(models.Model):
    title = models.CharField('Название', max_length=250)
    description = models.TextField('Описание')
    date = models.DateTimeField('Дата')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class Modules(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField('Название модуля', max_length=250)
    description = models.TextField('Описание модуля')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

class Lessons(models.Model):
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField('Название урока', max_length=250)
    content = models.TextField('Содержание урока')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

class Assignment(models.Model):
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField('Название задания', max_length=250)
    description = models.TextField('Описание задания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
#Запись на курсы
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

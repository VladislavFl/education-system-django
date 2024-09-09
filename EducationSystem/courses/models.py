from django.db import models

class Courses(models.Model):
    title = models.CharField('Название', max_length=250)
    description = models.TextField('Описание')
    date = models.DateTimeField('Дата')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

from django.contrib import admin
from .models import Courses, Modules, Lessons, Assignment, Enrollment, CourseProgress

admin.site.register(Courses)
admin.site.register(Modules)
admin.site.register(Lessons)
admin.site.register(Assignment)
admin.site.register(Enrollment)
admin.site.register(CourseProgress)
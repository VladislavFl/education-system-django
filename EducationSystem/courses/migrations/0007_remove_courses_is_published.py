# Generated by Django 5.1.1 on 2024-09-12 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_courses_is_published_alter_modules_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courses',
            name='is_published',
        ),
    ]

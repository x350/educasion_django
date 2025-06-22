from django.db import models
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


# Create your models here.
# UserModel = get_user_model()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название дисциплины')

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название курса')
    description = models.TextField(null=False, blank=True, verbose_name='Описание курса')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created']



class Lesson(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название урока')
    description = models.TextField(null=False, blank=True, verbose_name='Описание урока')
    teacher = models.OneToOneField(Teacher, on_delete=models.DO_NOTHING)
    photo = models.ImageField(null=True, upload_to='photos/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['pk']


class StudentsGroup(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name='students')


def lesson_files_path(instance: "LessonFiles", filename: str) -> str:
    return "courses/course_{pk}/files/{filename}".format(
        pk=instance.lesson.pk,
        filename=filename
    )


class LessonFiles(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=lesson_files_path)
    description = models.CharField(max_length=200, null=False, blank=True)

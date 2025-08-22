from django.contrib.auth import admin
from django.db import models
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse_lazy


# Create your models here.
# UserModel = get_user_model()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy('education:student_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['user']

    def __str__(self):
        if not self.user.last_name:
            return self.user.username
        else:
            return ' '.join([self.user.first_name, self.user.last_name])


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy('education:teacher_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['user']

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название дисциплины')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created']

    title = models.CharField(max_length=200, unique=True, verbose_name='Название курса')
    description = models.TextField(null=False, blank=True, verbose_name='Описание курса')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses', verbose_name='Категория')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    students = models.ManyToManyField(Student, related_name='courses', blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name='Активный курс')

    def short_description(self):
        return self.description[:50] + ' ... .'

    def get_absolute_url(self):
        return reverse_lazy('education:course_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название урока')
    description = models.TextField(null=False, blank=True, verbose_name='Описание урока')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lessons', verbose_name='Преподаватель')
    photo = models.ImageField(null=True, upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фотография')
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='lessons',
                               blank=True,
                               null=True,
                               verbose_name='Курс',
                               )

    def short_description(self):
        return self.description[:50] + ' ... .'

    def get_absolute_url(self):
        return reverse_lazy('education:lesson_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['pk']


# class StudentsGroup(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name='students')


def lesson_files_path(instance: "LessonFiles", filename: str) -> str:
    return "lessons/lessons_{pk}/files/{filename}".format(
        pk=instance.lesson.pk,
        filename=filename
    )


class LessonFiles(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=lesson_files_path)
    description = models.CharField(max_length=200, null=False, blank=True)

    def __str__(self):
        return f'Файлы урока {self.lesson.title}'

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['pk']

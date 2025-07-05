from django.core.management.base import BaseCommand

from education.models import Lesson, Course, Teacher, Student, LessonFiles


class Command(BaseCommand):

    def simple_filtres(self):
        course = Course.objects.get(pk=1)
        users = course.lesson_set.all()
        op_qs = Lesson.objects.all()
        # op_qs = Lesson.LessonFiles_set()
        # for op in op_qs:
        # self.stdout.write(f'{op_qs[0].files.get_queryset()[0].file}')
        self.stdout.write(f'{users[0]}')


    def handle(self, *args, **kwargs):
        # self.stdout.write(self.style).NOTICE('Start commands...')

        self.simple_filtres()

        # self.stdout.write(self.style).SUCCESS('Start commands...')


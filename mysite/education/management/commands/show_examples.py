from django.core.management.base import BaseCommand

from education.models import Lesson, Course, Teacher, Student, LessonFiles


class Command(BaseCommand):

    def simple_filtres(self):
        item = Student.objects.get(pk=1)


        # op_qs = Lesson.LessonFiles_set()
        # for op in op_qs:
        # self.stdout.write(f'{op_qs[0].files.get_queryset()[0].file}')
        # qs = item.field.name
        qs = item.courses.all()
        self.stdout.write(f'{qs}')


    def handle(self, *args, **kwargs):
        # self.stdout.write(self.style).NOTICE('Start commands...')

        self.simple_filtres()

        # self.stdout.write(self.style).SUCCESS('Start commands...')


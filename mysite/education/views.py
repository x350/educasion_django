
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import View
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, DeleteView
from .models import Course, Lesson, Student, Teacher, LessonFiles
from .forms import CourseForm, LessonForm
from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView


class LessonItemInline(InlineFormSetFactory):
    model = Lesson
    fields = '__all__'
    form_class = LessonForm
    factory_kwargs = {'extra': 1}


class CoursesListView(ListView):
    model = Course
    template_name = "education/course_list.html"
    context_object_name = 'courses'
    # extra_context = {'title': 'Наши курсы'}
    paginate_by = 3

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Course.objects.all()
        else:
            return Course.objects.filter(students=self.request.user.pk)


class CourseDetailView(DetailView):
    model = Course
    template_name = "education/course_detail.html"
    context_object_name = 'course'


class CourseCreateView(CreateWithInlinesView):
    model = Course
    form_class = CourseForm
    inlines = [LessonItemInline]
    template_name = 'education/course_create.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class CourseUpdateView(UpdateWithInlinesView):
    model = Course
    form_class = CourseForm
    inlines = [LessonItemInline]
    # fields = '__all__'
    template_name = 'education/course_update.html'
    context_object_name = 'course'

    def get_success_url(self):
        return reverse_lazy('education:course_detail', kwargs={'pk': self.object.pk})


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('education:courses_list')


class TeachersListView(ListView):
    model = Teacher
    context_object_name = 'teachers'
    template_name = "education/teachers_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Наши преподаватели'
        return context


class TeacherDetailView(DetailView):
    queryset = (
        Teacher.objects
        .select_related("user")
    )
    context_object_name = 'teacher'
    template_name = "education/teacher_detail.html"


class StudentsListView(ListView):
    model = Student
    context_object_name = 'students'
    template_name = "education/student_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Наши студенты'
        return context


class StudentDetailView(DetailView):
    queryset = (
        Student.objects
        .select_related("user")
        . prefetch_related("courses")
    )
    context_object_name = 'student'
    template_name = "education/student_detail.html"


class LessonListView(ListView):
    model = Lesson
    template_name = "education/lesson_list.html"
    context_object_name = 'lessons'
    # extra_context = {'title': 'Наши курсы'}
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Наши курсы'
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(is_active=True)


class LessonDetailView(DetailView):
    # model = Lesson
    queryset = (
        Lesson.objects
        .select_related("course")
        .select_related("teacher")
        .prefetch_related("files")
    )
    template_name = "education/lesson_detail.html"
    context_object_name = 'lesson'


class LessonFilesItemInline(InlineFormSetFactory):
    model = LessonFiles
    fields = ['lesson', 'file', 'description']
    factory_kwargs = {'extra': 2}


class LessonCreateView(CreateWithInlinesView):
    model = Lesson
    inlines = [LessonFilesItemInline]
    fields = ['title', 'course', 'description', 'teacher', 'photo', ]
    template_name = 'education/lesson_create.html'
    context_object_name = 'lesson'

    def get_initial(self):
        initial = super().get_initial()
        course_pk = self.kwargs.get('pk')
        initial['course'] = Course.objects.get(pk=course_pk)
        # print('pk - ', initial['course'].pk, course_pk)
        return initial

    def get_success_url(self):
        return reverse_lazy('education:course_detail', kwargs={'pk': self.object.course.pk})


class LessonUpdateView(UpdateWithInlinesView):
    model = Lesson
    template_name = 'education/lesson_update.html'
    inlines = [LessonFilesItemInline]
    fields = '__all__'
    context_object_name = 'lesson'

    def get_success_url(self):
        return reverse_lazy('education:lesson_detail', kwargs={'pk': self.object.pk})


class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'education/lesson_delete.html'

    def get_success_url(self):
        return reverse_lazy('education:course_detail', kwargs={'pk': self.object.course.pk})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегестрировались.')
            return redirect('education:index')
        else:
            messages.error(request, "Ошибка валидации.")
    else:
        form = UserRegisterForm()
    return render(request, 'education/register.html', {'form': form})


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('education:login')

    def post(self, request):
        logout(request)
        return redirect('education:login')


class IndexListView(ListView):
    model = Course
    template_name = "education/index_course_list.html"
    context_object_name = 'courses'
    # extra_context = {'title': 'Наши курсы'}
    paginate_by = 3







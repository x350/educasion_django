from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Course, Lesson, Student, Teacher
from .forms import CourseForm, LessonFormSet, LessonFilesFormSet

# Create your views here.
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    # fields = 'title', 'description', 'category', 'is_active', #'__all__'
    template_name = 'education/create_course.html'
    success_url = reverse_lazy('education:courses_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['lesson_formset'] = LessonFormSet(self.request.POST)
        else:
            context['lesson_formset'] = LessonFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        lesson_formset = context['lesson_formset']
        if lesson_formset.is_valid():
            self.object = form.save()
            lesson_formset.instance = self.object
            lesson_formset.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    # fields = "__all__"
    template_name = "education/course_update.html"


class TeachersListView(ListView):
    model = Teacher
    context_object_name = 'teachers'
    template_name = "education/teachers_list.html"


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
    # queryset = (
    #     Student.objects
    #     .select_related("user")
    # )

class StudentDetailView(DetailView):
    queryset = (
        Student.objects
        .select_related("user")
        . prefetch_related("courses")
    )
    context_object_name = 'student'
    template_name = "education/student_detail.html"

class CoursesListView(ListView):
    model = Course
    template_name = "education/course_list.html"
    context_object_name = 'courses'
    # extra_context = {'title': 'Наши курсы'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Наши курсы'
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Course.objects.filter(is_active=True) # реализовать выбор курсов конкретного пользователя
        else:
            return Course.objects.filter(is_active=True)

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return HttpResponseForbidden()
    #     return super(CoursesView, self).dispatch(request, *args, **kwargs)


class CourseDetailView(DetailView):
    model = Course
    template_name = "education/course_detail.html"
    context_object_name = 'course'




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


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('education:index')
    else:
        form = UserLoginForm()

    return render(request, 'education/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('education:login')


def index(request):
    return render(request, 'education/index.html')

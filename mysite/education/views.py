from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectMixin

from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, FormView
from .models import Course, Lesson, Student, Teacher, LessonFiles
from .forms import CourseForm, LessonForm, LessonFormSet, LessonFilesFormSet
from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView


# Create your views here.

# class UserAccessMixin(PermissionRequiredMixin):
#     def dispatch(self, request, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return redirect_to_login(self.request.get_full_path(),
#                                      self.get_login_url(), self.get_redirect_field_name())
#
#         if not self.has_permission():
#             return redirect('education:index')
#
#         return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class LessonItemInline(InlineFormSetFactory):
    model = Lesson
    fields = '__all__'
    form_class = LessonForm
    factory_kwargs = {'extra': 1}


class LessonFilesItemInline(InlineFormSetFactory):
    model = LessonFiles
    fields = '__all__'
    factory_kwargs = {'extra': 1}


class CourseCreateView(CreateWithInlinesView):
    model = Course
    form_class = CourseForm
    inlines = [LessonItemInline]
    # fields = '__all__'
    template_name = 'education/course_create.html'
    # success_url = reverse_lazy('education:courses_list')

    def get_success_url(self):
        return self.object.get_absolute_url()

    def forms_valid(self, form, inlines):
        response = self.form_valid(form)
        for formset in inlines:
            formset.save()
        return response


class CourseUpdateView(UpdateWithInlinesView):
    model = Course
    form_class = CourseForm
    inlines = [LessonItemInline]
    # fields = '__all__'
    template_name = 'education/course_update.html'
    success_url = reverse_lazy('education:courses_list')


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('education:courses_list')


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
    paginate_by = 2
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
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Наши курсы'
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Course.objects.all() # реализовать выбор курсов конкретного пользователя
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
            return Lesson.objects.all() # реализовать выбор курсов конкретного пользователя
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


class LessonUpdateView(UpdateWithInlinesView):
    model = Lesson
    template_name = 'education/lesson_update.html'
    inlines = [LessonFilesItemInline]
    fields = '__all__'
    success_url = reverse_lazy('education:lesson_detail')
    context_object_name = 'lesson'


class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'education/lesson_delete.html'
    # fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('education:course_detail', kwargs={'pk': self.object.course.pk})
    # context_object_name = 'lesson'


    # def form_valid(self, form):
    #     success_url = self.get_success_url()
    #     self.object.is_active = False
    #     self.object.save()
    #     return HttpResponseRedirect(success_url)





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

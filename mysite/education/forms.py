from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django_select2.forms import Select2MultipleWidget, Select2Widget
from .models import Course, Lesson, Student, Teacher, LessonFiles
from django.forms import inlineformset_factory


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))



# class StudentWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "user__icontains",
#         # "first_name__icontains",
#         # "last_name__icontains",
#         # "email__icontains",
#     ]

#
# class LessonWidget(s2forms.ModelSelect2MultipleWidget):
#     search_fields = [
#         "title__icontains",
#         "description__icontains",
#         "teacher__icontains",
#     ]
#
class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = "__all__"

    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=Select2MultipleWidget,
        label='Студенты',
        required=False,

    )
    lesson = forms.ModelMultipleChoiceField(
        queryset=Lesson.objects.all(),
        widget=Select2MultipleWidget,
        label='Уроки',
        required=False,
    )


LessonFormSet = inlineformset_factory(
    Course,
    Lesson,
    fields=('title', 'description', 'teacher', 'photo',),
    extra=1,
    can_delete=False,
)

LessonFilesFormSet = inlineformset_factory(
    Lesson,
    LessonFiles,
    fields=('lesson', 'file', 'description'),
    extra=1,
    can_delete=False,

)
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from nested_admin import NestedModelAdmin, NestedTabularInline, NestedStackedInline
from .models import Course, Student, Teacher, Lesson, Category, LessonFiles


# Register your models here.


# class LessonsCourseInline(admin.StackedInline):
#     model = Lesson
#     fields = "title", 'description', 'teacher', 'photo',
#     # inlines = [LessonInline]


class StudentInline(NestedStackedInline):
    model = Course.students.through
    extra = 1

@admin.action(description='Deactivtion')
def mark_deactivate(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_active=False)

@admin.action(description='Activtion')
def mark_activate(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_active=True)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "title",
    list_display_links = "title",


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = "user__username", 'user__first_name', 'user__last_name'
    list_display_links = "user__username", 'user__first_name', 'user__last_name'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = "user__username", 'user__first_name', 'user__last_name'
    list_display_links = "user__username", 'user__first_name', 'user__last_name'


class LessonFilesInline(NestedStackedInline):
    model = LessonFiles
    extra = 1
    # model = Lesson.files
    fields = 'file', 'description'


# @admin.register(Lesson)
# class LessonAdmin(admin.ModelAdmin):
#     model = Lesson
#     list_display = "pk", "title", "description", "teacher", "photo", 'course'
#     inlines = [
#         LessonFilesInline,
#     ]
#     list_display_links = "pk", "title",

class LessonInLine(NestedStackedInline):
    model = Lesson
    extra = 1
    list_display = "pk", "title", "description", "teacher", "photo", 'course'
    inlines = [
        LessonFilesInline,
    ]
    list_display_links = "pk", "title",



@admin.register(Course)
class CourseAdmin(NestedModelAdmin):
    actions = [
        mark_deactivate,
        mark_activate
    ]
    list_display = "pk", "title", "description", "category",  "created", "update", "is_active"
    list_display_links = "pk", "title", "category", "is_active"
    ordering = "pk", "-title"
    search_fields = "title", "description",

    inlines = [
        StudentInline,
        LessonInLine,
    ]
@admin.register(Lesson)
class LessonAdmin(NestedModelAdmin):
    list_display =  "pk", "title", "description", "teacher", "photo", "course"
    list_display_links = "title",
    inlines = [
        LessonFilesInline,
    ]


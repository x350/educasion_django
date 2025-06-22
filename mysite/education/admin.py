from django.contrib import admin
from .models import Course, Student, Teacher, Lesson, Category, LessonFiles


# Register your models here.
class LessonInline(admin.TabularInline):
    model = LessonFiles


# class StudentInline(admin.StackedInline):
#     model = StudentsGroup


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "description", "category", "created", "update", "is_active"
    list_display_links = "pk", "title", "category", "is_active"
    ordering = "pk", "-title"
    search_fields = "title", "description",

    inlines = [
        # StudentInline
    ]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "description", "teacher", "photo",
    inlines = [
        LessonInline,
    ]
    list_display_links = "pk", "title",


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "title",
    list_display_links = "title",


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass

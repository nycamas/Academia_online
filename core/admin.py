from django.contrib import admin
from .models import User, Course, Lesson, Enrollment, Evaluation, Score

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'date_joined')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'duration', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'content')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'progress', 'enrolled_at')
    list_filter = ('status', 'enrolled_at')
    search_fields = ('student__username', 'course__title')

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'max_score')
    list_filter = ('course', 'due_date')
    search_fields = ('title', 'description')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'evaluation', 'score', 'submitted_at')
    list_filter = ('evaluation', 'submitted_at')
    search_fields = ('student__username', 'evaluation__title')

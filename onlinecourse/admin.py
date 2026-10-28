"""Django administration for course content and assessments.

Repository: https://github.com/jatinmahire/tfjzl-final-cloud-app-with-database
Public source: https://github.com/jatinmahire/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/admin.py

The seven model imports below are registered with the Django admin site.
QuestionInline edits course questions, ChoiceInline edits question answers,
QuestionAdmin configures question editing, and LessonAdmin lists lessons.
"""

from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'grade']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)

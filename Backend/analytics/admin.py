from django.contrib import admin
from quizzes.models import TestResult


class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'quiz', 'score', 'correct_answers', 'date_passed')
    list_filter = ('company', 'quiz', 'date_passed')
    search_fields = ('user__username', 'company__name', 'quiz__title')


admin.site.register(TestResult, TestResultAdmin)

from django import forms
from django.contrib import admin
from quizzes.models import TestResult, Question as CustomQuestion, Answer as CustomAnswer


class AnswerInline(admin.StackedInline):
    model = CustomAnswer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = CustomAnswer
        fields = ['answer_text', 'is_correct']


class AnswerAdmin(admin.ModelAdmin):
    form = AnswerForm


class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'quiz', 'score', 'date_passed')
    list_filter = ('company', 'quiz', 'date_passed')
    search_fields = ('user__username', 'company__name', 'quiz__title', 'quiz__questions__question_text')

    def get_correct_answers(self, obj):
        return ", ".join(obj.quiz.answers_ref.values_list('answer_text', flat=True))

    get_correct_answers.short_description = 'Correct Answers'


# Remove the previous registrations for Question and Answer
admin.site.unregister(CustomQuestion)
admin.site.unregister(CustomAnswer)

# Register the updated models
admin.site.register(CustomQuestion, QuestionAdmin)
admin.site.register(TestResult, TestResultAdmin)
admin.site.register(CustomAnswer, AnswerAdmin)

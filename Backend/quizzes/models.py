from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from companies.models import Company


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    frequency = models.IntegerField(default=0)
    associated_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    answers_ref = models.ManyToManyField('Answer', related_name='question_set', blank=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.answer_text


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField()
    correct_answers = models.IntegerField(default=0)
    date_passed = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"Result for {self.user.username} in {self.question.quiz.title}"


class LastTestTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    last_test_time = models.DateTimeField()

    def __str__(self):
        return f"Last test time for {self.user.username} in {self.quiz.title}"



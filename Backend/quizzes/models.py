from django.db import models
from django.contrib.auth.models import User
from companies.models import Company


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    frequency = models.PositiveIntegerField()  # Number indicating the frequency of taking the quiz in days

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    correct_answers = models.IntegerField()

    def __str__(self):
        return f"Result for {self.user.username} in {self.quiz.title}"


class LastTestTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    last_test_time = models.DateTimeField()

    def __str__(self):
        return f"Last test time for {self.user.username} in {self.quiz.title}"



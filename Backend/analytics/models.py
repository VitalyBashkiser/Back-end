from django.db import models
from django.contrib.auth.models import User


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    average_score = models.FloatField()


class QuizCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.CASCADE)
    completion_time = models.DateTimeField()

    class Meta:
        permissions = [
            ("view_quiz_completion", "Can view quiz completion"),
        ]


class AverageScores(models.Model):
    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.CASCADE)
    average_score = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f'{self.quiz.title} - {self.date}'
from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    frequency = models.PositiveIntegerField()  # Number indicating the frequency of taking the quiz in days

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    answers_ref = models.ManyToManyField('Answer', related_name='question_set', blank=True)

    def selected_answers(self):
        return self.answers.filter(is_correct=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question_ref = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


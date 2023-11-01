from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from datetime import datetime
from .models import Rating, QuizCompletion, AverageScores
from quizzes.models import Quiz
from django.urls import reverse


class AnalyticsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаем тестовых пользователей
        self.user = User.objects.create(username='testuser')

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Создаем тестовые данные для Rating
        Rating.objects.create(user=self.user, average_score=8.5)

        # Создаем тестовые данные для QuizCompletion
        quiz = Quiz.objects.create(title='Test Quiz', description='Test description', frequency=7)
        QuizCompletion.objects.create(user=self.user, quiz=quiz, completion_time=datetime.now())

        # Создаем тестовые данные для AverageScores
        AverageScores.objects.create(quiz=quiz, average_score=7.5)

    def test_get_rating(self):
        url = reverse('rating-list')  # Use the name from your urls.py
        response = self.client.get(url)
        print(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_quiz_completions(self):
        url = reverse('quizcompletion-list')  # Use the name from your urls.py
        response = self.client.get(url)
        print(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_average_scores(self):
        url = reverse('quiz-averagescores-list')  # Use the name from your urls.py
        response = self.client.get(url)
        print(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


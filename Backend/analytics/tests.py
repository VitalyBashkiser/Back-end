from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from main.models import User
from .models import AverageScores, QuizCompletion
from quizzes.models import Quiz
from django.urls import reverse
from django.utils import timezone


class AnalyticsTests(TestCase):
    def setUp(self):
        # Create a test user and authenticate them
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.user_id = self.user.id  # Added line to get the user's id

    def test_get_rating(self):
        url = reverse('rating-list')  # Use the name from your urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_quiz_completions(self):
        # Create a quiz for the user to complete
        quiz = Quiz.objects.create(title='Test Quiz', description='Test description', frequency=7)

        # Create a QuizCompletion for the user
        QuizCompletion.objects.create(user=self.user, quiz=quiz, completion_time=timezone.now())

        url = reverse('quizcompletion-list')  # Use the name from your urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_average_scores(self):
        # Create a quiz for average scores
        quiz = Quiz.objects.create(title='Test Quiz', description='Test description', frequency=7)

        # Create an AverageScores record
        AverageScores.objects.create(quiz=quiz, average_score=7.5)

        url = reverse('quiz-averagescores-list')  # Use the name from your urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


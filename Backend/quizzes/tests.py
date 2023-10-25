import random
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from companies.models import Company
from .models import Quiz
from .views import calculate_average_score, expected_average_score


class QuizTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create(username='testuser')
        # Create a company
        self.company = Company.objects.create(name='Test Company', owner=self.user)
        # Create a quiz
        self.quiz = Quiz.objects.create(title='Test Quiz', description='Test Description', frequency=7)

    def test_start_quiz(self):
        response = self.client.post(reverse('start-quiz', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quiz started successfully")

    def test_record_test_result(self):
        # Simulate user taking a quiz and answering questions
        data = {
            'user_id': self.user.id,
            'company_id': self.company.id,
            'quiz_id': self.quiz.id,
            'score': random.randint(0, 100),
            'correct_answers': random.randint(0, 10)  # Simulated correct answers
        }

        response = self.client.post(reverse('record-test-result'), data, format='json')
        self.assertEqual(response.status_code, 201)

        # Verify that the average score is calculated correctly
        average_score = calculate_average_score(self.user)
        self.assertEqual(average_score, expected_average_score(0, 0))

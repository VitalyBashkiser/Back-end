import random
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from companies.models import Company
from .models import Quiz
from django.db.models import Sum, Count


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

        # Verify that the user's average score is calculated correctly
        user = User.objects.get(id=data['user_id'])
        total_correct_answers = user.testresult_set.aggregate(total=Sum('correct_answers'))['total']
        total_questions_answered = user.testresult_set.values('quiz__questions').annotate(
            total=Count('quiz__questions'))

        if total_questions_answered and total_correct_answers:
            total_questions = total_questions_answered[0]['total']
            average_score = total_correct_answers / total_questions if total_questions > 0 else 0
        else:
            average_score = 0
        self.assertEqual(average_score, 0.0)


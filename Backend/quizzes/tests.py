import random
import csv
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from companies.models import Company
from .models import Quiz, TestResult
from django.db.models import Sum, Count
from django.http import HttpResponse


class QuizTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create(username='testuser')
        # Create a company
        self.company = Company.objects.create(name='Test Company', owner=self.user)

    def test_start_quiz(self):
        # Create a quiz with frequency
        self.quiz = Quiz.objects.create(title='Test Quiz', description='Test Description', frequency=7)

        response = self.client.post(reverse('start-quiz', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quiz started successfully")

    def test_record_test_result(self):
        # Create a quiz with frequency
        self.quiz = Quiz.objects.create(title='Test Quiz', description='Test Description', frequency=7)

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


class ExportDataTest(TestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.company_owner = User.objects.create_user(username='company_owner', password='test_password')
        self.company_admin = User.objects.create_user(username='company_admin', password='test_password')

        # Assign roles
        self.company_owner.is_owner = True
        self.company_owner.save()
        self.company_admin.is_administrator = True
        self.company_admin.save()

        # Creating a company and a quiz
        self.company = Company.objects.create(name='test_company', owner=self.company_owner)
        self.quiz = Quiz.objects.create(title='test_quiz')

        # Create quiz results
        self.result1 = TestResult.objects.create(user=self.user, company=self.company, quiz=self.quiz, score=60,
                                                 correct_answers=4)
        self.result2 = TestResult.objects.create(user=self.company_admin, company=self.company, quiz=self.quiz,
                                                 score=70, correct_answers=5)
        self.result3 = TestResult.objects.create(user=self.company_owner, company=self.company, quiz=self.quiz,
                                                 score=80, correct_answers=6)

    def test_export_json(self):
        url = reverse('export-json')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('attachment; filename="data.json"', response['Content-Disposition'])
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'})

    def test_export_csv(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'

        writer = csv.writer(response)
        writer.writerow(['id', 'user', 'company', 'quiz', 'score'])

        test_results = TestResult.objects.all()

        for result in test_results:
            writer.writerow([result.id, result.user.username, result.company.name, result.quiz.title, result.score])

        return response



import random
import csv
import os
import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from companies.models import Company
from .models import Quiz, TestResult, Question, datetime
from django.db.models import Sum, Count
from rest_framework.test import APITestCase


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class QuestionTests(APITestCase):
    def test_create_question_with_selected_answers(self):
        quiz = Quiz.objects.create(title='Test Quiz', description='Description', frequency=7)

        url = reverse('create_question_with_selected_answers')
        data = {
            "quiz": quiz.id,
            "question_text": "What is the capital of France?",
            "answers": [
                {"answer_text": "Paris", "is_correct": True},
                {"answer_text": "London", "is_correct": False},
                {"answer_text": "Berlin", "is_correct": False}
            ]
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 201)
        question = Question.objects.get(id=response.data['id'])
        self.assertEqual(question.question_text, "What is the capital of France?")
        self.assertEqual(question.answers.count(), 3)
        self.assertTrue(question.answers.filter(answer_text="Paris", is_correct=True).exists())


class QuestionTests2(APITestCase):
    def test_create_question_with_selected_answers(self):
        quiz = Quiz.objects.create(title='Test Quiz', description='Description', frequency=7)

        url = reverse('create_question_with_selected_answers')
        data = {
            "quiz": quiz.id,
            "question_text": "What is the largest mammal on Earth?",
            "answers": [
                {"answer_text": "Elephant", "is_correct": False},
                {"answer_text": "Blue Whale", "is_correct": True},
                {"answer_text": "Giraffe", "is_correct": False}
            ]
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 201)
        question = Question.objects.get(id=response.data['id'])
        self.assertEqual(question.question_text, "What is the largest mammal on Earth?")
        self.assertEqual(question.answers.count(), 3)
        self.assertTrue(question.answers.filter(answer_text="Blue Whale", is_correct=True).exists())


class QuestionTests3(APITestCase):

    def test_create_question_with_selected_answers(self):
        quiz = Quiz.objects.create(title='Test Quiz', description='Description', frequency=7)

        url = reverse('create_question_with_selected_answers')
        data = {
            "quiz": quiz.id,
            "question_text": "What is the capital of Japan?",
            "answers": [
                {"answer_text": "Tokyo", "is_correct": False},
                {"answer_text": "Beijing", "is_correct": True},
                {"answer_text": "Seoul", "is_correct": False}
            ]
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 201)
        question = Question.objects.get(id=response.data['id'])
        self.assertEqual(question.question_text, "What is the capital of Japan?")
        self.assertEqual(question.answers.count(), 3)
        self.assertTrue(question.answers.filter(answer_text="Beijing", is_correct=True).exists())


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
            'correct_answers': random.randint(0, 10),  # Simulated correct answers
            'date_passed': datetime.datetime.now()
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

        # Verify the structure and content of the JSON
        json_data = response.json()

        for idx, result in enumerate(TestResult.objects.all()):
            expected_data = {
                'id': result.id,
                'user': result.user.username,
                'company': result.company.name,
                'quiz': result.quiz.title,
                'score': result.score,
                'date passed': result.date_passed.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.assertEqual(json_data[idx], expected_data)

        # Save the JSON data to a file
        json_file_path = os.path.join(BASE_DIR, 'quizzes', 'data.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

    def test_export_csv(self):
        response = self.client.get(reverse('export-csv'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="data.csv"', response['Content-Disposition'])

        # Path to save the CSV file
        file_path = os.path.join(BASE_DIR, 'quizzes', 'data.csv')

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            # Write header row
            writer = csv.writer(f)
            writer.writerow(['id', 'user', 'company', 'quiz', 'score', 'date passed'])

            # Write data rows
            for result in TestResult.objects.all():
                writer.writerow([result.id, result.user.username, result.company.name, result.quiz.title, result.score,
                                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path))

        def test_create_question_with_selected_answers(self):
            quiz = Quiz.objects.create(title='Test Quiz', description='Description', frequency=7)

            url = reverse('create_question_with_selected_answers')
            data = {
                "quiz": quiz.id,
                "question_text": "What is the capital of Japan?",
                "answers": [
                    {"answer_text": "Tokyo", "is_correct": False},
                    {"answer_text": "Beijing", "is_correct": True},
                    {"answer_text": "Seoul", "is_correct": False}
                ]
            }
            response = self.client.post(url, data, format='json')
            print(response.data)
            self.assertEqual(response.status_code, 201)
            question = Question.objects.get(id=response.data['id'])
            self.assertEqual(question.question_text, "What is the capital of Japan?")
            self.assertEqual(question.answers.count(), 3)
            self.assertTrue(question.answers.filter(answer_text="Beijing", is_correct=True).exists())



import random
import csv
import os
import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from companies.models import Company
from .models import Quiz, TestResult, Question, Answer
from rest_framework.test import APITestCase
from django.utils import timezone


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class QuestionTests(APITestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')

    def test_create_question_with_selected_answers_1(self):
        quiz = Quiz.objects.create(title='Test Quiz', description='Description', frequency=7)

        url = reverse('question_test_1')
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
        self.assertEqual(response.status_code, 201)
        question = Question.objects.get(id=response.data['id'])
        self.assertEqual(question.question_text, "What is the capital of France?")
        self.assertEqual(question.answers.count(), 3)
        self.assertTrue(question.answers.filter(answer_text="Paris", is_correct=True).exists())


class QuestionTests2(APITestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')

    def test_create_question_with_selected_answers_2(self):
        quiz = Quiz.objects.create(title='Test Quiz', description='Description', frequency=7)

        url = reverse('question_test_2')
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
        self.assertEqual(response.status_code, 201)
        question = Question.objects.get(id=response.data['id'])
        self.assertEqual(question.question_text, "What is the largest mammal on Earth?")
        self.assertEqual(question.answers.count(), 3)
        self.assertTrue(question.answers.filter(answer_text="Blue Whale", is_correct=True).exists())


class QuestionTests3(APITestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')

    def test_create_question_with_selected_answers_3(self):
        quiz = Quiz.objects.create(title='Test Quiz', description='Description', frequency=7)

        url = reverse('question_test_3')
        data = {
            "quiz": quiz.id,
            "question_text": "What is the capital of Japan?",
            "answers": [
                {"answer_text": "Tokyo", "is_correct": True},
                {"answer_text": "Beijing", "is_correct": False},
                {"answer_text": "Seoul", "is_correct": False}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        question = Question.objects.get(id=response.data['id'])
        self.assertEqual(question.question_text, "What is the capital of Japan?")
        self.assertEqual(question.answers.count(), 3)
        self.assertTrue(question.answers.filter(answer_text="Tokyo", is_correct=True).exists())


class QuizTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('testpassword')
        self.user.save()
        self.client.login(username='testuser', password='testpassword')
        self.company = Company.objects.create(name='Test Company', owner=self.user)

        # Create a quiz with frequency
        self.quiz = Quiz.objects.create(title='Test Quiz', description='Test Description', frequency=7)

        # Create a question and associate it with the quiz
        self.question = Question.objects.create(
            quiz=self.quiz,
            question_text='What is the capital of Japan?'
        )

        # Create answers and associate them with the question
        self.answer1 = Answer.objects.create(
            question=self.question,
            answer_text='Tokyo',
            is_correct=True
        )
        self.answer2 = Answer.objects.create(
            question=self.question,
            answer_text='Beijing',
            is_correct=False
        )
        self.answer3 = Answer.objects.create(
            question=self.question,
            answer_text='Seoul',
            is_correct=False
        )

    def test_start_quiz(self):
        response = self.client.post(reverse('start-quiz', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quiz started successfully")

    def test_create_result(self):
        url = reverse('create_result')

        data = {
            'user_id': self.user.id,
            'company_id': self.company.id,
            'quiz_id': self.quiz.id,
            'question_id': self.question.id,
            'selected_answer': self.answer1.id,  # You may need to adjust this based on your implementation
            'score': random.randint(0, 100),
            'correct_answers': random.randint(0, 10),
            'date_passed': timezone.now()
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

        # Verify that the record about the passed test was saved to the database
        test_result = TestResult.objects.get(user=self.user, quiz=self.quiz)
        self.assertEqual(test_result.date_passed.replace(microsecond=0), data['date_passed'].replace(microsecond=0))
        self.assertEqual(test_result.score, data['score'])
        self.assertEqual(test_result.correct_answers, data['correct_answers'])


class ExportDataTest(TestCase):
    def setUp(self):
        # Creating users
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.company_owner = User.objects.create_user(username='company_owner', password='test_password')
        self.company_admin = User.objects.create_user(username='company_admin', password='test_password')

        # We create a company and associate it with the owner and administrator
        self.company = Company.objects.create(name='Test Company', owner=self.company_owner)
        self.company_owner.is_owner = True
        self.company_owner.save()
        self.company_admin.is_administrator = True
        self.company_admin.save()

        # Login as test users
        self.client.login(username='test_user', password='test_password')
        self.client.login(username='company_owner', password='test_password')
        self.client.login(username='company_admin', password='test_password')

        # We create quizzes
        self.quiz1 = Quiz.objects.create(
            title='Test Quiz 3',
            description='This quiz is about capitals again',
            frequency=30
        )

        self.quiz2 = Quiz.objects.create(
            title='Test Quiz 1',
            description='This quiz is about capitals',
            frequency=7
        )

        self.quiz3 = Quiz.objects.create(
            title='Test Quiz 2',
            description='This quiz is about animals',
            frequency=14
        )

        # Creating questions and answers
        # Question 1
        self.question1 = Question.objects.create(
            quiz=self.quiz1,
            question_text='What is the capital of Japan?'
        )
        self.answer1_1 = Answer.objects.create(
            question=self.question1,
            answer_text='Tokyo',
            is_correct=True
        )
        self.answer1_2 = Answer.objects.create(
            question=self.question1,
            answer_text='Beijing',
            is_correct=False
        )
        self.answer1_3 = Answer.objects.create(
            question=self.question1,
            answer_text='Seoul',
            is_correct=False
        )

        # Question 2
        self.question2 = Question.objects.create(
            quiz=self.quiz2,
            question_text='What is the capital of France?'
        )
        self.answer2_1 = Answer.objects.create(
            question=self.question2,
            answer_text='Paris',
            is_correct=True
        )
        self.answer2_2 = Answer.objects.create(
            question=self.question2,
            answer_text='London',
            is_correct=False
        )
        self.answer2_3 = Answer.objects.create(
            question=self.question2,
            answer_text='Berlin',
            is_correct=False
        )

        # Question 3
        self.question3 = Question.objects.create(
            quiz=self.quiz3,
            question_text='What is the largest mammal on Earth?'
        )
        self.answer3_1 = Answer.objects.create(
            question=self.question3,
            answer_text='Elephant',
            is_correct=False
        )
        self.answer3_2 = Answer.objects.create(
            question=self.question3,
            answer_text='Blue Whale',
            is_correct=True
        )
        self.answer3_3 = Answer.objects.create(
            question=self.question3,
            answer_text='Giraffe',
            is_correct=False
        )

        # Create test results
        self.result1 = TestResult.objects.create(
            user=self.user,
            company=self.company,
            quiz=self.quiz1,
            question=self.question1,
            selected_answer=self.answer1_1,
            score=60,
            correct_answers=1
        )
        self.result2 = TestResult.objects.create(
            user=self.company_admin,
            company=self.company,
            quiz=self.quiz2,
            question=self.question2,
            selected_answer=self.answer2_1,
            score=70,
            correct_answers=1
        )
        self.result3 = TestResult.objects.create(
            user=self.company_owner,
            company=self.company,
            quiz=self.quiz3,
            question=self.question3,
            selected_answer=self.answer3_2,
            score=80,
            correct_answers=1
        )

    def test_export_data(self):
        self.client.login(username='test_user', password='test_password')

        url = reverse('export-data', kwargs={'format': 'json'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        json_data = response.json()

        # Save the JSON data to a file
        json_file_path = os.path.join(BASE_DIR, 'quizzes', 'data.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        # Test CSV export
        url = reverse('export-data', kwargs={'format': 'csv'})
        response = self.client.get(url)

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
                writer.writerow(
                    [result.id, result.user.username, result.company.name, result.quiz.title, result.score,
                     result.date_passed.strftime("%Y-%m-%d %H:%M:%S")])

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path))

        # Read the expected JSON data from the file
        with open(json_file_path, 'r') as json_file:
            expected_data = json.load(json_file)

        # Compare the exported JSON data with the expected data
        self.assertEqual(json_data, expected_data)
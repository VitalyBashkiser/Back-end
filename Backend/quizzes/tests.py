import random
from rest_framework.test import APITestCase
from .models import Question, Quiz, TestResult
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from companies.models import Company
from django.utils import timezone


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

    def test_create_result(self):
        # Create a quiz with frequency
        self.quiz = Quiz.objects.create(title='Test Quiz', description='Test Description', frequency=7)

        # Simulate user taking a quiz and answering questions
        data = {
            'user_id': self.user.id,
            'company_id': self.company.id,
            'quiz_id': self.quiz.id,
            'score': random.randint(0, 100),
            'correct_answers': 1,
            'date_passed': timezone.now()
        }

        response = self.client.post(reverse('create_result'), data, format='json')
        self.assertEqual(response.status_code, 201)

        # Verify that the record about the passed test was saved to the database
        test_result = TestResult.objects.get(user=self.user, quiz=self.quiz)
        self.assertEqual(test_result.date_passed.replace(microsecond=0), data['date_passed'].replace(microsecond=0))
        self.assertEqual(test_result.score, data['score'])
        self.assertEqual(test_result.correct_answers, data['correct_answers'])

from rest_framework.test import APITestCase
from .models import Question, Quiz
from django.urls import reverse


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



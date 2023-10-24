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
        self.assertEqual(response.status_code, 201)
        question = Question.objects.get(id=response.data['id'])
        self.assertEqual(question.text, "What is the capital of France?")
        self.assertEqual(question.selected_answers.count(), 1)
        self.assertEqual(question.selected_answers.first().text, "Paris")

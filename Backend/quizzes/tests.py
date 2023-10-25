from django.test import TestCase
from django.urls import reverse
import random


class QuizTests(TestCase):

    def test_start_quiz(self):
        response = self.client.post(reverse('start-quiz', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quiz started successfully")

    def test_record_test_result(self):
        data = {
            'user_id': 1,
            'company_id': 1,
            'quiz_id': 1,
            'score': random.randint(0, 100)
        }

        response = self.client.post(reverse('record-test-result'), data, format='json')
        self.assertEqual(response.status_code, 201)

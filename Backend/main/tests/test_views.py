from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class UserAPITestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_get_user_by_id(self):
        url = reverse('get_user_by_id', kwargs={'user_id': self.user.id})
        response = self.client.get(url)

        # Check that the request returned a status of 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the user data matches the expected data
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['username'], self.user.username)
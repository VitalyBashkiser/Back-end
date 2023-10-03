from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class CreateUserAPITestCase(TestCase):
    def test_create_user(self):
        url = reverse('user-list')  # Assuming you have a URL named 'user-list' for creating users
        data = {
            'username': 'newuser',
            'password': 'newpassword'
        }

        response = self.client.post(url, data, format='json')

        # Check that the request returned a status of 201 Created (since it's creating a new resource)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the user was created in the database
        self.assertTrue(User.objects.filter(username='newuser').exists())

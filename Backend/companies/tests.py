from rest_framework.test import APITestCase
from rest_framework import status
from .models import Company, User, Invitation, Request
from django.urls import reverse


class CompanyActionsTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='test_password')
        self.user = User.objects.create_user(username='user', password='test_password')
        self.company = Company.objects.create(name='Test Company', owner=self.owner)
        self.invitation = Invitation.objects.create(user=self.user, company=self.company)
        self.request = Request.objects.create(user=self.user, company=self.company)

    def test_send_invitations(self):
        self.client.force_authenticate(user=self.owner)
        invited_users = [self.user.id]
        url = reverse('send_invitations', args=[self.company.id])
        response = self.client.post(url, {'invited_users': invited_users}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invitation.objects.count(), 2)

    def test_revoke_invitation(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse('revoke_invitation', args=[self.company.id, self.invitation.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Invitation.objects.filter(id=self.invitation.id).exists())

    def test_approve_request(self):
        url = reverse('approve_request', args=[self.company.id, self.request.id])
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.request.refresh_from_db()
        self.assertEqual(self.request.status, 'APPROVED')
        self.assertTrue(self.company.members.filter(id=self.user.id).exists())

    def test_remove_user_from_company(self):
        other_user = User.objects.create_user(username='other_user', password='other_user')
        self.company.members.add(other_user)
        self.client.force_authenticate(user=self.owner)
        url = reverse('remove_user_from_company', args=[self.company.id, other_user.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.company.members.filter(id=other_user.id).exists())


class UserActionsTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='test_password')
        self.user = User.objects.create_user(username='user', password='test_password')
        self.company = Company.objects.create(name='Test Company', owner=self.owner)
        self.invitation = Invitation.objects.create(user=self.user, company=self.company)
        self.request = Request.objects.create(user=self.user, company=self.company)
        self.company.members.add(self.user)

    def test_accept_invitation(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('accept_invitation', args=[self.company.id, self.invitation.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.company.members.filter(id=self.user.id).exists())
        self.assertFalse(Invitation.objects.filter(id=self.invitation.id).exists())

    def test_send_request(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('send_request', args=[self.company.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Request.objects.count(), 2)

    def test_cancel_request(self):
        self.client.force_authenticate(user=self.user)
        self.request = Request.objects.create(user=self.user, company=self.company)
        url = reverse('cancel_request', args=[self.company.id, self.request.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(Request.DoesNotExist):
            Request.objects.get(id=self.request.id)

    def test_decline_invitation(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('decline_invitation', args=[self.company.id, self.invitation.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(Invitation.DoesNotExist):
            Invitation.objects.get(id=self.invitation.id)

    def test_leave_company(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('leave_company', args=[self.company.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.company.members.filter(id=self.user.id).exists())

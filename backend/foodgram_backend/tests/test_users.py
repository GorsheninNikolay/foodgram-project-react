from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APITestCase
from users.models import User


class UserTestCase(APITestCase):

    data = {
            'email': 'vpupkin@yandex.ru',
            'username': 'vasya.pupkin',
            'first_name': 'Вася',
            'last_name': 'Пупкин',
            'password': 'Qwerty123'
            }

    def setUp(self):
        self.user = User.objects.create(
            email='tester@yandex.ru',
            username='tester',
            first_name='Test',
            last_name='Testovich',
            password='test'
        )
        self.token = Token.objects.create(
            user=self.user
        )
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list_of_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_of_users_by_unathorized_client(self):
        self.client.credentials()
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration(self):
        response = self.client.post('/api/users/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_profile(self):
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

    def test_profile_another_person(self):
        self.client.post('/api/users/', self.data)
        response = self.client.get('/api/users/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 2)

    def test_profile_unathorized_client(self):
        self.client.credentials()
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_set_password(self):
        old_password = self.user.password
        passwords = {
            'new_password': 'new',
            'current_password': 'test'
        }
        response = self.client.post('/api/users/set_password/', passwords)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(old_password, self.user.password)

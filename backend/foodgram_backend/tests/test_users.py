from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory, APITestCase
from users.models import Follow, User


class UserTestCase(APITestCase):

    data = {
            'email': 'vpupkin@yandex.ru',
            'username': 'vasya.pupkin',
            'first_name': 'Вася',
            'last_name': 'Пупкин',
            'password': 'Qwerty123'
            }

    def setUp(self):
        self.user_tester = User.objects.create(
            email='tester@yandex.ru',
            username='tester',
            first_name='Test',
            last_name='Testovich',
            password='test'
        )
        self.user_another = User.objects.create(
            email='another@yandex.ru',
            username='another',
            first_name='Another',
            last_name='Tester',
            password='another'
        )
        self.token = Token.objects.create(
            user=self.user_tester
        )
        self.token_another = Token.objects.create(
            user=self.user_another
        )
        self.client = APIClient()
        self.another_client = APIClient()
        self.unathorized_client = APIClient()
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.another_client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_another.key
            )
        self.unathorized_client.credentials()

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
        self.assertEqual(User.objects.all().count(), 3)

    def test_profile(self):
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['username'], 'tester')
        self.assertNotEqual(response.data['username'], 'vasya.pupkin')

    def test_profile_another_person(self):
        response = self.client.get('/api/users/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 2)

    def test_profile_unathorized_client(self):
        response = self.unathorized_client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_set_password(self):
        old_password = self.user_tester.password
        passwords = {
            'new_password': 'new',
            'current_password': 'test'
        }
        response = self.client.post('/api/users/set_password/', passwords)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(old_password, User.objects.get(id=1).password)

    def test_get_token(self):
        self.client.post('/api/users/', self.data)
        email_password = {
            'email': self.data['email'],
            'password': self.data['password']
        }
        response = self.client.post('/api/auth/token/login/', email_password)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(Token.objects.all().count(), 3)

    def test_delete_token_by_owner(self):
        response = self.client.post('/api/auth/token/logout/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Token.objects.all().count(), 1)

#    def test_subscriptions(self):

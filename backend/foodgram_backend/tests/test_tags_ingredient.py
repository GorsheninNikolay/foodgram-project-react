from django.db import IntegrityError, transaction
from recipe.models import Ingredient, Tag
# from recipe.exceptions import SubscribeOnYourSelf, UniqueObjectDoesntWork
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from users.models import User


class RecipeTestCase(APITestCase):

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
        self.ingredient = Ingredient.objects.create(
            name='test_ingredient',
            measurment_unit='test_measurment'
        )
        self.tag = Tag.objects.create(
            name='test_tag',
            color='#00A00B',
            slug='test_slug'
        )
        self.token = Token.objects.create(
            user=self.user_tester
        )
        self.unathorized_client = APIClient()
        self.unathorized_client.credentials()
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_ingredients(self):
        response = self.unathorized_client.get('/api/ingredients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ingredient.objects.all().count(), 1)
        self.assertEqual(response.data[0]['name'], 'test_ingredient')
        self.assertEqual(response.data[0]['id'], 1)

    def test_get_one_ingredient(self):
        response = self.unathorized_client.get('/api/ingredients/1/')
        self.assertEqual(Ingredient.objects.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_ingredient')
        self.assertEqual(response.data['id'], 1)

    def test_try_create_ingredient(self):
        response = self.client.post('/api/ingredients/')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
            )
        self.assertEqual(Ingredient.objects.all().count(), 1)

    def test_get_tags(self):
        response = self.unathorized_client.get('/api/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.all().count(), 1)
        self.assertEqual(response.data[0]['name'], 'test_tag')

    def test_get_one_tag(self):
        response = self.unathorized_client.get('/api/tags/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.all().count(), 1)
        self.assertEqual(response.data['name'], 'test_tag')

    def test_create_tag(self):
        response = self.client.post('/api/tags/')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
            )
        self.assertEqual(Tag.objects.all().count(), 1)

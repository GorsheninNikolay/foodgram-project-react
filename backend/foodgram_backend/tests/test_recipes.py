import logging
import os
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from foodgram_backend.settings import MEDIA_ROOT
from PIL import Image
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from users.models import Follow, User


class RecipeTestCase(APITestCase):

    data = {
        'ingredients': [
            {
                'id': 1,
                'amount': 555
            }
            ],
        'tags': [
            1
        ],
        'image': r'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==', # noqa
        'name': 'test',
        'text': 'test',
        'cooking_time': 5
        }

    another_data = {
        'ingredients': [
            {'id': 1, 'amount': 999},
            {'id': 2, 'amount': 999}
            ],
        'tags': [
            1,
            2
        ],
        'image': r'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==', # noqa
        'name': 'another',
        'text': 'another',
        'cooking_time': 999
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
        self.ingredient = Ingredient.objects.create(
            name='test_ingredient',
            measurement_unit='test_measurment'
        )
        self.ingredient2 = Ingredient.objects.create(
            name='test_ingredient2',
            measurement_unit='test_ingredient2'
        )
        self.tag = Tag.objects.create(
            name='test_tag',
            color='#00A00B',
            slug='test_slug'
        )
        self.another_tag = Tag.objects.create(
            name='test_tag_2',
            color='#11B11C',
            slug='test_slug_2'
        )
        self.first_recipe = Recipe.objects.create(
            author=self.user_tester,
            name='first_recipe',
            image=tempfile.NamedTemporaryFile(suffix='.jpg').name,
            text='first_recipe',
            cooking_time=10
        )
        self.recipe_ingredient = RecipeIngredient.objects.create(
                recipe=self.first_recipe, ingredient=self.ingredient, amount=10
                )
        self.first_recipe.tags.set(Tag.objects.filter(id=1))
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

    def tearDown(self):
        try:
            os.remove('media/images/another.png')
        except FileNotFoundError:
            pass
        try:
            os.remove('media/images/test.png')
        except FileNotFoundError:
            pass

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.another_client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_another.key
            )
        self.unathorized_client.credentials()

    def test_get_recipes(self):
        response = self.unathorized_client.get(r'/api/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_recipe(self):
        response = self.client.post(r'/api/recipes/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.all().count(), 2)

    def test_get_recipe(self):
        response = self.unathorized_client.get(r'/api/recipes/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_recipe(self):
        self.client.post(r'/api/recipes/', self.data, format='json')
        self.assertEqual(Recipe.objects.all().count(), 2)
        response = self.client.put(
            r'/api/recipes/2/', self.another_data, format='json'
            )
        recipe = Recipe.objects.get(id=2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.all().count(), 2)
        self.assertEqual(recipe.name, self.another_data['name'])
        self.assertEqual(
            recipe.cooking_time, self.another_data['cooking_time']
            )
        self.assertEqual(recipe.text, self.another_data['text'])
        self.assertTrue(recipe.name in recipe.image.path)
        self.assertEqual(recipe.ingredients.count(), 2)

    def test_put_recipe_by_unauth_user(self):
        response = self.unathorized_client.put(
            r'/api/recipes/1/', self.another_data, format='json'
            )
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(recipe.name, self.another_data['name'])
        self.assertNotEqual(
            recipe.cooking_time, self.another_data['cooking_time']
            )
        self.assertNotEqual(recipe.text, self.another_data['text'])

    def test_put_recipe_by_another_user(self):
        response = self.another_client.put(
            r'/api/recipes/1/', self.another_data, format='json'
            )
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(recipe.name, self.another_data['name'])
        self.assertNotEqual(
            recipe.cooking_time, self.another_data['cooking_time']
            )
        self.assertNotEqual(recipe.text, self.another_data['text'])

    def test_delete_recipe(self):
        self.client.post(r'/api/recipes/', self.data, format='json')
        self.assertEqual(Recipe.objects.all().count(), 2)
        response = self.client.delete(r'/api/recipes/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.all().count(), 1)

    def test_delete_recipe_by_another_user(self):
        response = self.another_client.delete(r'/api/recipes/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Recipe.objects.all().count(), 1)

    def test_delete_non_exist_recipe(self):
        response = self.client.delete(r'/api/recipes/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Recipe.objects.all().count(), 1)

    def test_create_favorite(self):
        response = self.client.get(r'/api/recipes/1/favorite/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favorite.objects.all().count(), 1)

    def test_create_double_favorite(self):
        self.client.get(r'/api/recipes/1/favorite/')
        response = self.client.get(r'/api/recipes/1/favorite/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Favorite.objects.all().count(), 1)

    def test_create_favorite_by_unath_user(self):
        response = self.unathorized_client.get(r'/api/recipes/1/favorite/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Favorite.objects.all().count(), 0)

    def test_delete_favorite(self):
        self.client.get(r'/api/recipes/1/favorite/')
        response = self.client.delete(r'/api/recipes/1/favorite/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Favorite.objects.all().count(), 0)

    def test_create_shopping_cart(self):
        response = self.client.get(r'/api/recipes/1/shopping_cart/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShoppingCart.objects.all().count(), 1)

    def test_create_double_shopping_cart(self):
        self.client.get(r'/api/recipes/1/shopping_cart/')
        response = self.client.get(r'/api/recipes/1/shopping_cart/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShoppingCart.objects.all().count(), 1)

    def test_create_shopping_cart_by_unauth_user(self):
        response = self.unathorized_client.get(
            r'/api/recipes/1/shopping_cart/'
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(ShoppingCart.objects.all().count(), 0)

    def test_delete_shopping_cart(self):
        self.client.get(r'/api/recipes/1/shopping_cart/')
        response = self.client.delete(r'/api/recipes/1/shopping_cart/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ShoppingCart.objects.all().count(), 0)

    def test_download_shopping_cart(self):
        self.client.get(r'/api/recipes/1/shopping_cart/')
        response = self.client.get(r'/api/recipes/download_shopping_cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

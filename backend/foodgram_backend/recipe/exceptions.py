from rest_framework.exceptions import APIException


class UniqueObjectsException(APIException):
    status_code = 400
    default_detail = 'Данный рецепт уже добавлен в избранное'

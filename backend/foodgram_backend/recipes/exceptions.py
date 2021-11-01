from rest_framework.exceptions import APIException


class UniqueObjectsException(APIException):
    status_code = 400
    default_detail = 'Данный объект уже существует'


class UniqueObjectDoesntWork(APIException):
    status_code = 400
    default_detail = 'Уникальный объект был создан повторно'


class SubscribeOnYourSelf(APIException):
    status_code = 400
    default_detail = 'Пользователь подписался на самого себя'

import base64

from django.core.files.base import ContentFile


def get_image(data):
    """ Преобразование кода base64 в картинку ContentFile """
    if (isinstance(data['image'], str)
            and data['image'].startswith('data:image')):
        format, imgstr = data['image'].split(';base64,')
        ext = format.split('/')[-1]
        return ContentFile(
            base64.b64decode(imgstr), name=data['name'] + '.' + ext
            )
    return None

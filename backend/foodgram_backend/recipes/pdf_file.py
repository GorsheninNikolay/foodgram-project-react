from django.http import HttpResponse


def create_shopping_cart(data):
    lines = []
    for record in data.values():
        lines.append(f"{record['name']} ({record['measurement_unit']}) -- {record['amount']}")  # noqa
    response_content = '\n'.join(lines)
    response = HttpResponse(response_content,
                            content_type='text/plain,charset=utf8')
    response['Content-Disposition'] = 'attachment; filename=shopping_cart.txt'
    return response

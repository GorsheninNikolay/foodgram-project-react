from io import BytesIO

from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def create_shopping_cart(data):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=shopping_cart.pdf'
    buffer = BytesIO()
    pen = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Bitter',
                                   'recipes/Font/Bitter-Medium.ttf'))
    pen.setFont('Times-Roman', 18)
    pen.drawString(100, 800, 'Foodgram_Project')
    pen.line(10, 790, 550, 790)
    height = 760
    pen.setFont('Bitter', 12)
    counter = 1
    for record in data.values():
        pen.drawString(45, height, f"{counter}. {record['name']} "
                                   f"({record['measurement_unit']})"
                                   f" -- {record['amount']}")
        if counter == 50:
            pen.showPage()
        height -= 15
        counter += 1
    pen.line(10, height, 790, height)
    pen.save()
    response.write(buffer.getvalue())
    buffer.close()
    return response

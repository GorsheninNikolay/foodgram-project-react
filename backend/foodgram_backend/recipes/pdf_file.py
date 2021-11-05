from fpdf import FPDF


def create_shopping_cart(data):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('times', size=18)
    pdf.cell(80, 10, txt='Foodgram_Project', ln=1, align='C')
    pdf.set_line_width(0.25)
    pdf.line(15, 20, 190, 20)
    pdf.set_font('times', size=16)
    for record in data.values():
        counter = 10
        pdf.cell(
            counter, 10,
            txt=f"{chr(32) * 8} {record['name']} ({record['measurement_unit']}) -- {record['amount']}", # noqa
            ln=5)
        counter += 2
    return pdf.output('media/shopping_cart.pdf')

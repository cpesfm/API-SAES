#AUTOR: El Diegongo
#Modificacion: Yo Mero

from PyPDF2                    import PdfWriter, PdfReader
from reportlab.pdfgen          import canvas
from reportlab.lib.pagesizes   import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase         import pdfmetrics
import io


CIFRAS_DESPUES_DEL_DECIMAL = 2

#info = {
#    'Name': 'Nombre Completo',
#    'ID': '1517459847',
#    'school_email': 'qwdfrr3400',
#    'personal_email': 'email@gmail.com',
#    'phone': '5563262184',
#    'admission_month': '08',
#    'admission_year': '2022',
#    'number_semester': 2,
#    'aproved_num': 12,
#    'academic_program': 4,
#    'credit_total': 105.00,
#}

semester_position = {
    1: 308,
    2: 327,
    3: 346,
    4: 365,
    5: 382,
    6: 401,
    7: 420,
    8: 439,
    9: 458,
    10: 483,
    11: 507,
    12: 532,
}

program_position = {
    1: [72, 322],
    2: [72, 275],
    3: [72, 236],
    4: [72, 202],
    5: [327, 322],
    6: [327, 275],
    7: [327, 236],
}

program_credits = {
    1: 312,
    2: 312,
    3: 316,
    4: 309,
    5: 318,
    6: 336,
    7: 394,
}


class main:
    def trunc(self, f, n=CIFRAS_DESPUES_DEL_DECIMAL):
        s = '{}'.format(f)
        if 'e' in s or 'E' in s:
            return '{0:.{1}f}'.format(f, n)
        i, p, d = s.partition('.')
        return '.'.join([i, (d+'0'*n)[:n]])
    def crear_pdf_carga_ac(self, info):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("roboto", 10) 
        can.drawString(65, 605, info['name'])
        can.drawString(395, 605, info['ID'])
        can.drawString(65, 561, info['school_email'])
        can.drawString(260, 561, info['personal_email'])
        can.drawString(450, 561, info['phone'])
        can.drawString(360, 525, info['admission_month'])
        can.drawString(475, 525, info['admission_year'])
        can.setFont("roboto", 20)
        can.drawString(semester_position[info['number_semester']], 480, 'X')
        can.setFont("roboto", 10)
        can.drawString(430, 435, str(info['aproved_num']))
        can.drawString(480, 395, self.trunc(info['aproved_num']/info['number_semester']))
        can.setFont("roboto", 20)
        can.drawString(program_position[info['academic_program']][0], program_position[info['academic_program']][1], 'X')
        can.setFont("roboto", 10)
        can.drawString(420, 163, str(info['credit_total']))
        can.drawString(415, 73, self.trunc((program_credits[info['academic_program']]-info['credit_total'])/(12-info['number_semester']))) #??? 
        can.showPage()  
        can.drawString(65, 605, info['name']) # ??????
        can.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        output = PdfWriter()
        bytes_PDF = io.BytesIO()
        for i in range(len(self.base_pdf.pages)): 
            page = self.base_pdf.pages[i]
            page.merge_page(new_pdf.pages[i])
            output.add_page(page)
        output.write(bytes_PDF) #guardar pdf en memoria
        return bytes_PDF
        
    def __init__(self):
        print("(init) " + __name__)
        pdfmetrics.registerFont(TTFont('roboto', 'API/assets/Roboto-Regular.ttf'))
        self.base_pdf = PdfReader(open("API/assets/pdf_base.pdf", "rb"))
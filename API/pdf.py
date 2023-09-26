#AUTOR: El Diegongo
#Modificacion: Yo Mero

from PyPDF2                  import PdfWriter, PdfReader
from reportlab.pdfgen        import canvas
from reportlab.lib.pagesizes import letter
import io

#=================
font     = "Helvetica" #TODO:Usar una fuente de licencia libre
base_pdf = PdfReader(open("API/assets/pdf_base.pdf", "rb"))
#======================


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
    def crear_pdf_carga_ac(self, info):
        self.can.drawString(65, 605, info['name'])
        self.can.drawString(395, 605, info['ID'])
        self.can.drawString(65, 561, info['school_email'])
        self.can.drawString(260, 561, info['personal_email'])
        self.can.drawString(450, 561, info['phone'])
        self.can.drawString(360, 525, info['admission_month'])
        self.can.drawString(475, 525, info['admission_year'])
        self.can.setFont(font, 20)
        #self.can.drawString(semester_position[info['number_semester']], 480, 'X')
        self.can.setFont(font, 10)
        self.can.drawString(430, 435, str(info['aproved_num']))
        #self.can.drawString(480, 395, str((info['aproved_num']/info['number_semester'])))
        self.can.setFont(font, 20)
        #self.can.drawString(program_position[info['academic_program']][0], program_position[info['academic_program']][1], 'X')
        self.can.setFont(font, 10)
        self.can.drawString(420, 163, str(info['credit_total']))
        #descomentar al terminar las pruebas
        #self.can.drawString(415, 73, str((program_credits[info['academic_program']]-info['credit_total'])/(12-info['number_semester']))) 
        self.can.showPage()  
        self.can.drawString(65, 605, '')
        self.can.save()
        #move to the beginning of the StringIO buffer
        self.packet.seek(0)
        # create a new PDF with Reportlab
        new_pdf = PdfReader(self.packet)
        output = PdfWriter()
        bytes_PDF = io.BytesIO()
        # add the "watermark" (which is the new pdf) on the existing page
        for i in range(len(base_pdf.pages)): 
            page = base_pdf.pages[i]
            page.merge_page(new_pdf.pages[i])
            output.add_page(page)
        # finally, write "output" to a real file
        #output_stream = open("destination.pdf", "wb")
        #output.write(output_stream)
        output.write(bytes_PDF) #guardar pdf en memoria
        #output_stream.close()
        #bytes_PDF.seek(0)
        #return bytes_PDF.getvalue()
        return bytes_PDF
    def __init__(self):
        self.packet = io.BytesIO()
        self.can = canvas.Canvas(self.packet, pagesize=letter)
        self.can.setFont(font, 10) #TODO: 
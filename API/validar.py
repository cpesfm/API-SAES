from flask import make_response
import re

MAX_STR_SIZE = 200
#CAMPOS = [["name", "txt", 50], ["ID", "digit", 10], ["school_email", "mail", 50],["personal_email", "mail", 50],\
#			["phone", "str", 20] ,["admission_month", "str", 13], ["admission_year", "digit", 4], ["number_semester", "int", 20],\
#			["aproved_num", "int", 100], ["academic_program", "int", 7], ["credit_total", "float", 500.0]]

CAMPOS = {"name":["txt", 70],"ID":["digit", 10],"school_email":["mail", 50],"personal_email":["mail", 50],"phone":["str", 20],\
			"admission_month":["str", 13],"admission_year":["digit", 4],"number_semester":["int", 20],"aproved_num":["int", 100],\
			"academic_program":["int", 7],"credit_total":["float", 500.0]}


#============== strings ================
ERR_CARACTERES_NO_ADMITIDOS = "Escribiste caracteres no admitidos en algunos campos o no tiene formato adecuado"
ERR_CAMPOS_VACIOS = "Olvidaste rellenar los campos obligatorios"
ERR_KEY_NOT_IN_CAMPOS = "La informacion recibida no tiene formato correcto" #posible pentesting
ERR_KEY_TOO_LONG = "Hubo un error al procesar tu peticion" #definitivamente es pentesting
#=======================================

class valObj:
	def add(self, key, data):
		self.data[key] = data
		#self.data.append(data)
	def __init__(self, err=True):
		self.data = {}
		self.error = err
		self.error_response = ""

class main:
	def vyc(self, dato, tipo, d_size=MAX_STR_SIZE):
		if not isinstance(dato, str):return None
		if(len(dato)>MAX_STR_SIZE):return None
		match(tipo):
			case "digit":
				if dato.isdigit() and len(dato) <= d_size: return dato
				return None
			case "int":
				if dato.isdigit():
					dato = int(dato)
					return dato if dato <= d_size else None
				return None
			case "txt":
				if len(dato) > d_size: return None
				return None if self.reText.search(dato) == None else dato
			case "mail":
				if len(dato) > d_size: return None
				return None if self.reMail.search(dato) == None else dato
			case "float":
				if dato.replace(".", "", 1).isdigit() or dato.isdigit():
					return float(dato)
				return None
			case "str":
				if len(dato) > d_size: return None
				return None if self.reStr.search(dato) == None else dato
		return None
	#def validarBoletaAlumno(self, num):

	def validar_form(self, form_dict):
		r = valObj()
		for key in form_dict:
			if len(key) > 24:
				r.error_response = ERR_KEY_TOO_LONG
				return r
			if key in CAMPOS:
				tmp = self.vyc(form_dict[key], CAMPOS[key][0], CAMPOS[key][1])
				if tmp:
					r.add(key,tmp)
				else:
					r.error_response = ERR_CARACTERES_NO_ADMITIDOS
					return r
			else:
				r.error_response = ERR_KEY_NOT_IN_CAMPOS
				return r
		r.error = False
		return r


	def __init__(self):
		print("(init) " + __name__)
		self.reStr  = re.compile(r"^[a-zA-Z0-9| áéíóúÁÉÍÓÚ]+$", flags=0)
		self.reText = re.compile(r"^[a-zA-Z| áéíóúÁÉÍÓÚ]+$", flags=0)
		self.reMail = re.compile(r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$", flags=0)
		#self.reMailIPN = re.compile(r"" ,flags=0)




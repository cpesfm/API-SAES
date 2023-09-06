import re

MAX_STR_SIZE = 200


class main:
	def validarYconvertir(self, dato, tipo, d_size=MAX_STR_SIZE):
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
				if len(dato) >= d_size: return None
				return None if self.reText.search(dato) == None else dato
			case "mail":
				if len(dato) >= d_size: return None
				return None if self.reMail.search(dato) == None else dato
			case "float":
				if dato.replace(".", "", 1).isdigit() or dato.isdigit():
					return float(dato)
				return None
			case "str":
				if len(dato) >= d_size: return None
				return None if self.reStr.search(dato) == None else dato
		return None
	#def validarBoletaAlumno(self, num):
	def __call__(self, data):
		#Aqui procesar y validar el request
	def __init__(self):
		print("(init) " + __name__)
		self.reStr  = re.compile(r"^[a-zA-Z0-9| áéíóúÁÉÍÓÚ]+$", flags=0)
		self.reText = re.compile(r"^[a-zA-Z| áéíóúÁÉÍÓÚ]+$", flags=0)
		self.reMail = re.compile(r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$", flags=0)
		#self.reMailIPN = re.compile(r"" ,flags=0)




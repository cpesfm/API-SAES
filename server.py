#TODO: Aprender a programar bien
from API.webscr  import main              as saes
from API.webscr  import db_json_materias  as db
from API.pdf     import main              as generar_pdf
from API.validar import main              as validador
#===============================================================================
from flask        import Flask, render_template, request, Response, make_response, abort, jsonify, send_file
from urllib.parse import quote
from markupsafe   import escape
from random       import randint
import time


app = Flask(__name__)
config = {}

class _fila:
	#TODO: Mover este class a su propio modulo en API/
	def __init__(self):
		self.gID = 0
		self.clientes = {}
	def generarID(self, n=3):
		q = ""
		for o in range(0,n):
			p = randint(48,57) if randint(0,1) % 2 == 0 else randint(97,122) if randint(0,1) % 2 == 1 else randint(65, 90)
			q += chr(p)
		return q
	def agregar(self):
		print("add")
		self.update()
		self.gID += 1
		id = self.generarID(18)
		self.clientes[id] = [self.gID, time.time()]
		return id

	def eliminar(self, id):
		del self.clientes[id]
		self.gID -= 1
		self.update()

	def pos(self, id):
		self.update()
		return self.clientes[id][0]

	def update(self):
		#TODO: Escribir CORRECTACTAMENTE esta rutina (el dict puede ser modificado mientras es iterado, no no no)
		eph = time.time()
		tmp = [0, 0, 0] #ordenar, apartir de, restar
		tmp_rm = [] #guardar las keys de los cliente a borrar
		for cliente in self.clientes:
			if eph-self.clientes[cliente][1] >= 10: #quitar a los que su epoch sea mas antiguo a 10 seg
				self.gID -= 1
				tmp = [1, self.clientes[cliente][0], tmp[2]+1] if (self.clientes[cliente][0] < tmp[1]) else [1, tmp[1], tmp[2]+1]
				tmp_rm.append(cliente)
		for i in tmp_rm: #borrar los clientes marcados para eliminar
			del self.clientes[i]
		if tmp[0]:
			for cliente in self.clientes:
				if self.clientes[cliente][0] >= tmp[1]:
					self.clientes[cliente][0] = self.clientes[cliente][0] - tmp[2]
		
fila = _fila()
nav = "" #TODO: Hacer esto mas seguro


@app.route('/api/<request_type>', methods = ['POST']) #TODO: Escribir la API
def esta_es_la_api(request_type=""): # gen_pdf(datos) | autocomplete(string parcial) | leer_saes(fila_id)
	match(request_type):
		case("gen_pdf"):
			#TODO:sanitizar la info entrante
			#TODO:Validar informacion (lengths, datos numericos, etc)
			#TODO:Tratar adecuadamente peticiones JSON
			req_data = {}
			campos = [["name", "txt", 50], ["ID", "digit", 10], ["school_email", "mail", 50],["personal_email", "mail", 50],\
			["phone", "str", 20] ,["admission_month", "str", 13], ["admission_year", "digit", 4], ["number_semester", "int", 20],\
			["aproved_num", "int", 100], ["academic_program", "int", 7], ["credit_total", "float", 500.0]]
			for campo in campos:
				print(campo[0])
				dato = request.form.get(campo[0])
				if dato:
					dato = vyc(dato, campo[1],campo[2]) #vyc(campo, tipo, size)
					if dato == None:
						return "Escribiste caracteres no admitidos en algunos campos", 400
					req_data[campo] = dato
				#else:
					#req_data[campo] = "PENDIENTE"
				#return app.send_static_file('peticion_invalida.html'), 500 #Error, falta informacion
				return "Olvidaste rellenar los campos obligatorios", 400
			#TODO:Poner esto dentro de un try except por si acaso
			buffer = generar_pdf().crear_pdf_carga_ac(info=req_data) #objeto stringIO
			resp = make_response(buffer.getvalue())
			resp.headers["Content-Disposition"] = "attachment; filename=NUMERO_DE_BOLETA_Y_EPOCH.pdf"
			#no usar el mime de pdf porque el navegador lo abre en su lector integrado
			#resp.mimetype = "application/pdf"
			resp.mimetype = "application/octet-stream" #triggerear la descarga del pdf
			return resp
		case("autocomplete"):
			return None
		case("leer_saes"):
			return None
	#if request = GET
	#    return send_file(
   #     buffer,
   #     as_attachment=True,
   #     download_name='NUMER0_DE_BOLETA.PDF',
   #     mimetype='application/pdf'
   # )
	#pdf = generar_pdf().crear_pdf_carga_ac()
	return None


@app.route('/xhr', methods = ['POST', 'GET'])
def index_login():
	global nav
	if request.method == 'POST':
		if(request.headers.get("Content-Type") == "application/json"):
			data = request.json
		else:
			return jsonify({"err":1, "txt":"Request invalido"}), 520 #WTF?
		if "id" in data:
			if not (data.get("id") in fila.clientes):
				return jsonify({"err":1, "txt":"Tiempo limite de espera alcanzado. Intentalo de nuevo."}), 530
			match data.get("req"):
				case "alive":
					lugar = fila.pos(data.get("id"))
					if(lugar == 1):
						nav = saes(headless=config["headless"])
						if nav.errorMsg:
							fila.eliminar(data.get("id"))
							return jsonify({"err":1, "txt":nav.errorMsg}), 520
						imagen_captcha = nav.get_captcha()
						if nav.errorMsg:
							fila.eliminar(data.get("id"))
							return jsonify({"err":1, "txt":nav.errorMsg}), 520
						return jsonify({"img":"data:image/png;base64," + imagen_captcha}), 200
					else:
						return jsonify({"pos":lugar}), 530
				case "captcha":
					if( not (data.get("boleta") and data.get("password") and data.get("captcha")) ):
						fila.eliminar(data.get("id"))
						return jsonify({"error":"informacion de login incompleta"}), 505
					if(not (nav.login(boleta=data.get("boleta"), password=data.get("password"), captcha=data.get("captcha")))):
						fila.eliminar(data.get("id"))
						return jsonify({"error":nav.errorMsg}), 506
					d = nav.leer_datos()
					#r = quote(render_template('editar.html',\
					#	nombre=d[0],boleta=d[1],telefono=d[2],mail=d[3],ingreso_a=d[1][0:4], total_creditos=d[7],\
					#	acreditadas=d[6]))
					fila.clientes[data.get("id")].append(render_template('editar.html',\
					#r = quote(render_template('editar_base.html',\
							nombre=d[0],boleta=d[1],telefono=d[2],mail=d[3],ingreso_a=d[1][0:4], total_creditos=d[7],\
							acreditadas=d[6],num_periodos=d[5]))
					#return jsonify({"html":r}), 200
					return jsonify({"html":"ok"}), 200
				case _ :
					print("default")
					return ""
		else:
			id = fila.agregar()
			return jsonify({"id":id}), 200
	else:
		return "???", 666
	return ""



#TODO: Aceptar peticion post para que los ids temporales no se queden el historial
@app.route("/hoja", methods = ['GET'])
@app.route("/hoja/<cliente_id>", methods = ['GET'])
def hoja_inscripcion(cliente_id=""):
	if cliente_id == "":
		return render_template("editar.html", \
		nombre="",boleta="",telefono="",num_periodos=0) 
	if cliente_id in fila.clientes:
		print(cliente_id)
		render_template_temp = fila.clientes[cliente_id][2]
		fila.eliminar(cliente_id)
		return render_template_temp
	return app.send_static_file('peticion_invalida.html'), 500

@app.route("/test")
def testing_api():
	return app.send_static_file('editar_base.html'), 200


@app.route('/')
def pagina_principal():
	return app.send_static_file('login.html'), 200
	#r = make_response(render_template('login.html'))
	#return r, 200


@app.errorhandler(404)
def page_not_found(error):
	return "Not found :(", 404
	#return render_template("404.html"), 404



if __name__ == '__main__':
	#TODO: Implementar los argumentos:
	# debug true/false : imprimir mensajes de error especificos
	# online true/false : el server sera visible en localhost o en una interfaz publica
	# frontend true/false : permitir interactuar con el frontend de la API (web)
	vyc = validador()
	config["headless"] = True
	app.run(host="0.0.0.0", port=6969)
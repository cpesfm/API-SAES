#TODO: Aprender a programar bien
from API.webscr  import main              as webscr_mdl
from API.webscr  import db_json_materias  as db
from API.pdf     import main              as generar_pdf
from API.validar import main              as validador
from API.fila    import main              as fila_mdl
#===============================================================================
from flask        import Flask, render_template, request, Response, make_response, abort, jsonify, send_file
from urllib.parse import quote
from markupsafe   import escape
import time


app = Flask(__name__)
config = {}
		
nav = "" #TODO: Hacer esto mas seguro


@app.route('/api/<request_type>', methods = ['POST']) #TODO: Escribir la API
def esta_es_la_api(request_type=""): # gen_pdf(datos) | autocomplete(string parcial) | leer_saes(fila_id)
	match(request_type):
		case("gen_pdf"):
			#TODO:Poner esto dentro de un try except por si acaso
			content_type = request.headers.get("Content-Type")
			if(content_type == "application/json"):
				#el request es un json
				data = validar_input.validar_json(request.json)
			elif(content_type == "application/x-www-form-urlencoded"): #multipart/form-data
				#el request es un form
				data = validar_input.validar_form(request.form)
			else:
				return app.send_static_file('peticion_invalida.html'), 400
			if data.error:
				return data.error_response, 400
			buffer = pdf.crear_pdf_carga_ac(info=data.data)
			#resp = make_response(buffer.getvalue())
			#resp.headers["Content-Type"] = ""
			#resp.headers["X-Content-Type-Options"] = "nosniff"
			#resp.headers["Content-Disposition"] = "attachment; filename=NUMERO_DE_BOLETA_Y_EPOCH.pdf"
			#resp.headers["Content-Disposition"] = "attachment; filename=" + data.info["ID"] + "_" + fila.generarID() + ".pdf"
			#no usar el mime de pdf porque el navegador lo abre en su lector integrado
			#resp.mimetype = "application/pdf"
			#resp.mimetype = "application/octet-stream" #triggerear la descarga del pdf
			#return resp
			if buffer:
				return Response(buffer.getvalue(), mimetype="application/octet-stream",\
				headers={"Content-Disposition":"attachment; filename=" + data.data["ID"] + "_" + fila.generarID() + ".pdf",\
				"X-Content-Type-Options":"nosniff"})
			return app.send_static_file('peticion_invalida.html'), 400
		case("autocomplete"):
			return "TODO", 404
		case("leer_saes"):
			return "TODO", 404
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
						#nav = saes(headless=config["headless"])
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
	return app.send_static_file('peticion_invalida.html'), 400

@app.route("/testing/<test>")
def testing_api(test=""):
	match(test):
		case "editar":
			return app.send_static_file('editar_base.html'), 200
		case "pdf":
			return app.send_static_file('pdf_test.html'), 200
	return "hola", 200


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
	validar_input = validador()
	fila = fila_mdl()
	pdf = generar_pdf()
	saes = webscr_mdl()
	config["headless"] = True
	app.run(host="0.0.0.0", port=6969)
#TODO: Aprender a programar bien
from API.webscr import main as saes
#from API.pdf import main as pdf

from flask import Flask, render_template, request, Response, make_response, abort, jsonify
from urllib.parse import quote
from markupsafe import escape
from random import randint
import time


app = Flask(__name__)
<<<<<<< HEAD
<<<<<<< HEAD
config = {}
=======

>>>>>>> fdf2dd5 (Contenerizacion de la api)
=======
config = {}
>>>>>>> f164b79f0f3ebabb74c0462c6909b3830fc3bfd8


class _fila:
	#TODO: Mover este class a su propio modulo en API/
	def __init__(self):
		self.gID = 0
		self.clientes = {}
	def generarID(self, n=3):
		q = ""
		for o in range(0,n):
			p = randint(42,57) if randint(0,1) % 2 == 0 else randint(97,122) if randint(0,1) % 2 == 1 else randint(63, 90)
			q += chr(p)
		return q
	def agregar(self):
		print("add")
		self.update()
		self.gID += 1
		id = self.generarID(10)
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
		eph = time.time()-10
		tmp = [0, 0, 0] #ordenar, apartir de, restar
		for cliente in self.clientes:
			if self.clientes[cliente][1] <= eph: #quitar a los que su epoch sea mas antiguo a 10 seg
				self.gID -= 1
				tmp = [1, self.clientes[cliente][0], tmp[2]+1] if (self.clientes[cliente][0] < tmp[1]) else [1, tmp[1], tmp[2]+1]
				del self.clientes[cliente]
		if tmp[0]:
			for cliente in self.clientes:
				if self.clientes[cliente][0] >= tmp[1]:
					self.clientes[cliente][0] = self.clientes[cliente][0] - tmp[2]
		
fila = _fila()
nav = "" #TODO: Hacer esto mas seguro


@app.route('/api', methods = ['POST']) #TODO: Escribir la API
def api_():
	return None


@app.route('/xhr', methods = ['POST', 'GET'])
def index_login():
	global nav
	if request.method == 'POST':
		if(request.headers.get("Content-Type") == "application/json"):
			data = request.json
		else:
<<<<<<< HEAD
<<<<<<< HEAD
			return jsonify({"err":1, "txt":"Request invalido"}),  #WTF?
=======
			return jsonify({"err":1, "txt":"Request invalido"}), 500
>>>>>>> fdf2dd5 (Contenerizacion de la api)
=======
			return jsonify({"err":1, "txt":"Request invalido"}),  #WTF?
>>>>>>> f164b79f0f3ebabb74c0462c6909b3830fc3bfd8
		if "id" in data:
			if not (data.get("id") in fila.clientes):
				return jsonify({"err":1, "txt":"Tiempo limite de espera alcanzado. Intentalo de nuevo."}), 530
			match data.get("req"):
				case "alive":
					lugar = fila.pos(data.get("id"))
					if(lugar == 1):
<<<<<<< HEAD
<<<<<<< HEAD
						nav = saes(headless=config["headless"])
=======
						nav = saes()
>>>>>>> fdf2dd5 (Contenerizacion de la api)
=======
						nav = saes(headless=config["headless"])
>>>>>>> f164b79f0f3ebabb74c0462c6909b3830fc3bfd8
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
<<<<<<< HEAD
<<<<<<< HEAD
						return jsonify({"error":nav.errorMsg}), 506
					#TODO: escribir en API/webscr.py>main la rutina para extraer la info necesaria
					d = nav.leer_datos()
					r = quote(render_template('editar.html',\
					 nombre=d[0],\
					 boleta=d[1],\
					 tel=d[2],\
					 mail=d[3]))
=======
						return jsonify({"error":nav.errorMsg}), 506  
					#TODO: escribir en API/webscr.py>main la rutina para extraer la info necesaria
					r = quote(render_template('editar.html'))
>>>>>>> fdf2dd5 (Contenerizacion de la api)
=======
						return jsonify({"error":nav.errorMsg}), 506
					#TODO: escribir en API/webscr.py>main la rutina para extraer la info necesaria
					d = nav.leer_datos()
					r = quote(render_template('editar.html',\
					 nombre=d[0],\
					 boleta=d[1],\
					 tel=d[2],\
					 mail=d[3]))
>>>>>>> f164b79f0f3ebabb74c0462c6909b3830fc3bfd8
					return jsonify({"html":r}), 200
				case _ :
					print("default")
					return ""
		else:
			id = fila.agregar()
			return jsonify({"id":id}), 200
	else:
		return "???", 666
	return ""

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
<<<<<<< HEAD
<<<<<<< HEAD
	config["headless"] = True
=======
>>>>>>> fdf2dd5 (Contenerizacion de la api)
=======
	config["headless"] = True
>>>>>>> f164b79f0f3ebabb74c0462c6909b3830fc3bfd8
	app.run(host="0.0.0.0", port=6969)
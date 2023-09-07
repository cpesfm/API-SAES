from random import randint



class main:
	def __init__(self):
		print("(init) " + __name__)
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
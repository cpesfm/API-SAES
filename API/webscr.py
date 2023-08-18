from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
<<<<<<< HEAD
<<<<<<< HEAD
from selenium.webdriver.firefox.options import Options
=======
>>>>>>> fdf2dd5 (Contenerizacion de la api)
=======
from selenium.webdriver.firefox.options import Options
>>>>>>> f164b79f0f3ebabb74c0462c6909b3830fc3bfd8
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup as bs
#from selenium.common.exceptions import *
<<<<<<< HEAD
=======
from selenium.webdriver.firefox.options import Options


>>>>>>> fdf2dd5 (Contenerizacion de la api)



class main:
	def setError(self, msg, e):
		self.error = e
		self.errorMsg = msg
	def limpiarError(self):
		self.error = ""
		self.errorMsg = ""
	def cerrar(self):
			if self.error : print(self.error)
			self.navegador.close()
			self.navegador.quit()
<<<<<<< HEAD
<<<<<<< HEAD
	def __init__(self, headless=True):
=======
	def __init__(self):
>>>>>>> fdf2dd5 (Contenerizacion de la api)
=======
	def __init__(self, headless=True):
>>>>>>> f164b79f0f3ebabb74c0462c6909b3830fc3bfd8
		self.limpiarError()
		try:
			#TODO: Soporte para chromedriver
			options = Options()
<<<<<<< HEAD
<<<<<<< HEAD
			options.headless = headless
=======
			options.headless = True
>>>>>>> fdf2dd5 (Contenerizacion de la api)
=======
			options.headless = headless
>>>>>>> f164b79f0f3ebabb74c0462c6909b3830fc3bfd8
			self.navegador = webdriver.Firefox(options=options)
			self.navegador.set_page_load_timeout(6) #si en 6 segundos no responde, morir
			self.navegador.get("https://www.saes.esfm.ipn.mx/")
		except Exception as e:
			self.setError("El SAES no responde, (offline?)", e)
			self.cerrar()
	def get_captcha(self):
		self.limpiarError()
		try:
			captcha = WebDriverWait(self.navegador, 10).until(EC.visibility_of(self.navegador.find_element(By.CLASS_NAME, 'LBD_CaptchaImage')))
			captchab64 = captcha.screenshot_as_base64
		except Exception as e:
			print("error captcha")
			self.setError("Hubo un error al obtener el captcha del SAES", e)
			self.cerrar()
			return
		return captchab64
	def login(self, boleta="", password="", captcha=""):
		self.limpiarError()
		if(boleta == "" or password == "" or captcha == ""):
			self.setError("Informacion incompleta", None) #regresar a la fila?
			self.cerrar()
			return
		try: #Intentar escribir datos de acceso
			self.navegador.find_element(By.ID, "ctl00_leftColumn_LoginUser_UserName").send_keys(boleta)
			self.navegador.find_element(By.ID, "ctl00_leftColumn_LoginUser_Password").send_keys(password)
			self.navegador.find_element(By.ID, "ctl00_leftColumn_LoginUser_CaptchaCodeTextBox").send_keys(captcha)
			self.navegador.find_element(By.ID, "ctl00_leftColumn_LoginUser_LoginButton").click()
		except Exception as e:
			self.setError("Hubo un error al intentar usar tus credenciales.", e) #regresar a la fila?
			self.cerrar()
			return False
		try: #Verificar si el login fue exitoso, o no
			elem = WebDriverWait(self.navegador, 15).until(EC.any_of( #verificar si el inicio de sesion fue exitoso (o no)
				EC.presence_of_element_located((By.ID, "ctl00_mainCopy_FormView1")),
				EC.visibility_of_element_located((By.XPATH, "/html/body/form/div[3]/div[3]/div[1]/div[2]/div/div[2]/div/anonymoustemplate/table/tbody/tr/td/span"))
			))
			if(elem.tag_name == "span"): #no se pudo :(
				#leer el mensaje de error
				s = bs(elem.get_attribute("innerHTML"), features="html.parser")
				self.setError(s.get_text(" ", strip=True), None)
				self.cerrar()
				return False
			else: # we're in
				return True
		except Exception as e:
			self.setError("Hubo un error al determinar si el inicio de sesion fue correcto o no.", e)
			self.cerrar()
			return False
	def leer_datos(self):
		datos = {}
		self.navegador.get("https://www.saes.esfm.ipn.mx/Alumnos/info_alumnos/Datos_Alumno.aspx")
		# ^^^ Ir directamente a la info personal. Al mover el mouse en el menu
		# lateral un script hace que los atributos de ciertos elementos cambien.
		# Investigar si es necesario simular un click (o engañar al script)
		datos[0] = self.navegador.find_element(By.ID, "ctl00_mainCopy_TabContainer1_Tab_Generales_Lbl_Nombre").get_attribute('innerHTML') #Nombre
		datos[1] = self.navegador.find_element(By.ID, "ctl00_mainCopy_TabContainer1_Tab_Generales_Lbl_Boleta").get_attribute('innerHTML') #Boleta
		#ActionChains(self.navegador)\
		#	.context_click(self.navegador.find_element(By.ID, "__tab_ctl00_mainCopy_TabContainer1_Tab_Direccion"))\
		#	.perform() #Simular click
		# ^^^ No es necesario simular click. dejar el codigo por si acaso
		datos[2] = self.navegador.find_element(By.ID, "ctl00_mainCopy_TabContainer1_Tab_Direccion_Lbl_Tel").get_attribute('innerHTML') #telefono
		datos[3] = self.navegador.find_element(By.ID, "ctl00_mainCopy_TabContainer1_Tab_Direccion_Lbl_eMail").get_attribute('innerHTML') #email
		self.navegador.get("https://www.saes.esfm.ipn.mx/Alumnos/boleta/kardex.aspx") #Ir al kardex
		datos[4] = self.navegador.find_element(By.ID, "ctl00_mainCopy_Lbl_Carrera").get_attribute('innerHTML') #carrea (¿con especialidad?)
		
		#leer todas las tablas dentro del span id "ctl00_mainCopy_Lbl_Kardex" con bs4
		return datos
from selenium                           import webdriver
from selenium.webdriver.support         import expected_conditions as EC
from selenium.webdriver.support.ui      import WebDriverWait
from selenium.webdriver.firefox.options import Options as FFOps
from selenium.webdriver.chrome.options import Options as ChrOps
from selenium.webdriver.common.keys     import Keys
from selenium.webdriver.common.by       import By
#from selenium.webdriver                 import ActionChains
#from selenium.common.exceptions         import *
from bs4                                import BeautifulSoup       as bs
from pysondb                            import getDb

db_json_materias = getDb("API/assets/materias.json")


class main:
	def limpiarNavegador(self):
		#TODO: Limpiar cookies e historial
		self.navegador.delete_all_cookies()
	def setNav(self, name, headless=True):
		match(name):
			case "firefox":
				#TODO:verificar si hay geckodriver
				options = FFOps()
				options.headless = headless
				profile = webdriver.FirefoxProfile()
				profile.set_preference("browser.cache.disk.enable", False)
				profile.set_preference("browser.cache.memory.enable", False)
				profile.set_preference("browser.cache.offline.enable", False)
				profile.set_preference("network.http.use-cache", True)
				#driver = webdriver.Firefox(profile)
				#executable_path = "./geckodriver"
				self.navegador = webdriver.Firefox(profile, options=options)
			case "chrome":
				#TODO:verificar si hay chromedriver
				options = ChrOps()
				if headless : options.add_argument("--headless")
				options.add_experimental_option("detach", False)
				#executable_path="./chromedriver"
				self.navegador = webdriver.Chrome(options=options)
		raise Exception("Navegador no reconocido / no especificado")
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
	def __init__(self, navegador="firefox", headless=True):
		self.limpiarError()
		print("(init) " + __name__)
		#options = Options()
		#options.headless = headless
		#self.navegador = webdriver.Firefox(options=options)
		self.setNav(navegador, headless)
		self.navegador.set_page_load_timeout(6) #si en 6 segundos no responde, morir
		self.client_ID = ""
	def get_captcha(self):
		self.limpiarError()
		try:
			self.navegador.get("https://www.saes.esfm.ipn.mx/")
		except Exception as e:
			self.setError("El SAES no responde, (offline?)", e)
			self.cerrar()
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
		# ====== LEER KARDEX =====
		s = bs(self.navegador.page_source, features="html.parser")
		semestres = s.find(id="ctl00_mainCopy_Lbl_Kardex").find_all('table')
		datos[5] = str(len(semestres)) #cantidad de semestres que al menos ha cursado
		datos[6] = 0 #acreditadas
		datos[7] = 0 #creditos totales
		datos[8] = [] #lista de reprobadas
		for semestre in semestres:
			tr = semestre.find_all("tr")
			for i in range(2, len(tr)):
				td = tr[i].find_all("td")
				materia = db_json_materias.getByQuery({"codigo":td[0].text})[0]
				if(int(td[-1].text) >5):
					datos[7] += float(materia["creditos"])
					datos[6] += 1
				else:
					datos[8].append(materia)
					
		return datos
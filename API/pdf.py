#TODO: Generar pdf a partir de datos pasados al modulo

<<<<<<< HEAD
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import json
import os

class pdfGenerator:
	def __init__(self):
		self.generate()
	
	def generate(self, lista={}):
		# Read JSON containing Lorem Ipsum text
		with open('assets/lorem.json', 'r') as file:
			data = json.load(file)
			lorem_text = data['lorem']

		# Create PDF
		c = canvas.Canvas('output.pdf', pagesize=letter)
		width, height = letter

		# Add Lorem Ipsum text
		c.drawString(100, height - 100, lorem_text)

		# Add images with different opacities and positions
		images = ['assets/assets.jpg', 'assets/assets2.jpg', 'assets/assets3.jpg']
		opacities = [1, 0.8, 0.2]
		positions = [(100, height - 300), (300, height - 500), (500, height - 700)]
		texts = ["Text over Image 0", "Text over Image 1", "Text over Image 2"]

		for i, image_path in enumerate(images):
			img = Image.open(image_path).convert("RGBA")
			background = Image.new('RGBA', img.size, (255, 255, 255, 255)) # White background
			img_with_opacity = Image.blend(background, img, alpha=opacities[i])
			img_path_with_opacity = f'temp_image{i}.png'
			img_with_opacity.save(img_path_with_opacity)
			x, y = positions[i]
			c.drawImage(img_path_with_opacity, x, y, width=200, height=150)
			c.drawString(x + 10, y + 75, texts[i]) # Write text over the image

		# Save PDF
		c.save()

if __name__ == '__main__':
	pdfGenerator()
	# removing temp files
	for i in range(3):
		img_path_with_opacity = f'temp_image{i}.png'
		os.remove(img_path_with_opacity)
=======

class main:
	def __init__(self):
		#cargar el documento
	
	def generar(self, lista={}):
		return None
>>>>>>> fdf2dd5 (Contenerizacion de la api)

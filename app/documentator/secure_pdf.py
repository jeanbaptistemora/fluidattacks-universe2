# -*- coding: utf-8 -*-
"Clase para aseguridad un PDF de hallazgos"
import time
from pyPdf import PdfFileWriter, PdfFileReader
#pip install pypdf
class SecurePDF(object):
	"Agrega seguridad basica a los PDF"

	result_dir = ""
	watermark_tpl = ""
	secure_pdf_username = ""
	secure_pdf_filename = ""

	def __init__(self):
		"Constructor de la clase"
		self.base = "/usr/src/app/app/documentator/"
		self.watermark_tpl = self.base + "resources/presentation_theme/"
		self.watermark_tpl += "watermark_integrates_es.pdf"
		self.result_dir = self.base + "/results/"

	def create_full(self, username, basic_pdf_name):
		"Ejecuta el proceso de seguridad en un PDF"

		self.secure_pdf_username = username
		water_pdf_name = self.watermark(basic_pdf_name)
		self.secure_pdf_filename = self.lock(water_pdf_name)
		return self.result_dir + self.secure_pdf_filename

	def create_only_pass(self, username, basic_pdf_name):
		"Ejecuta el proceso de seguridad en un PDF"

		self.secure_pdf_username = username
		self.secure_pdf_filename = self.lock(basic_pdf_name)
		return self.result_dir + self.secure_pdf_filename


	def watermark(self, in_filename):
		"Agrega una marca de agua a todas las paginas de un PDF"

		pdf_foutname = "water_" + in_filename
		input = PdfFileReader(file(self.result_dir + in_filename, "rb")) # noqa
		output = PdfFileWriter()
		watermark = PdfFileReader(file(self.watermark_tpl, "rb"))
		for i in range(0, input.getNumPages()):
			overlay = watermark.getPage(0)
			page = input.getPage(i)
			page.mergePage(overlay)
			output.addPage(page)
		outputStream = file(self.result_dir + pdf_foutname, "wb")
		output.write(outputStream)
		outputStream.close()
		return pdf_foutname


	def lock(self, in_filename):
		" Agrega una clave a un PDF "

		pdf_foutname = self.secure_pdf_username + "_" + in_filename
		password = time.strftime("%d%m%Y") + self.secure_pdf_username.encode('utf8', 'ignore')
		print password
		output = PdfFileWriter()
		input = PdfFileReader(file(self.result_dir + in_filename, "rb")) # noqa
		for i in range(0, input.getNumPages()):
			output.addPage(input.getPage(i))
		outputStream = file(self.result_dir + pdf_foutname, "wb")
		output.encrypt(password, use_128bit=True)
		output.write(outputStream)
		outputStream.close()
		return pdf_foutname

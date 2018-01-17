# -*- coding: utf-8 -*-
" Clase para generar Excel de hallazgos "

from openpyxl import load_workbook
import re

class ITReport(object):
	workbook = None
	current_sheet = None
	data = None
	lang = None
	row = 3
	qc_row = 3
	result_filename = ""
	result_path = "/usr/src/app/app/techdoc/results/"
	templates = {
		'es': {
			'NOQC': "/usr/src/app/app/techdoc/templates/NOQC.xlsx",
			'QC': "/usr/src/app/app/techdoc/templates/QC.xlsx"
		},
		'en': {}}
	sheet_names = {
		'es': {
			'finding': 'Hallazgos',
			'qc_matriz': 'MatrizQC'
		},
		'en': {}}
	finding = {
		'name': 2,
		'description': 3,
		'where': 4,
		'where_records': 5,
		'requirements': 6,
		'measurements': 8,
		'criticity': 9,
		'cardinality': 10,
		'affected_records': 11,
		'evidence': 12,
		'solution': 13,
		'requirements_id': 15}
	matriz = {
		'type': 5,
		'component': 6,
		'requirements_id': 8,
		'requirements': 9,
		'scenario': 13,
		'ambit': 17,
		'category': 18,
		'threat': 19,
		'cssv2_value': 24,
		'probability': 26,
		'severity': 27,
		'risk': 30}

	def __init__(self, project, data, username, lang = "es"):
		self.lang = lang
		report_format = self.detect_format(data)
		self.generate(data, project, username, report_format)

	def detect_format(self, data):
		detailed = 0
		for finding in data:
			if finding["tipo"] =="Detallado":
				detailed += 1
		detailed = detailed * 100 / len(data)
		if detailed >= 50:
			self.workbook = load_workbook(
				filename = self.templates[self.lang]['QC']
			)
			return 'QC'
		self.workbook = load_workbook(
			filename = self.templates[self.lang]['NOQC']
		)
		return 'NOQC'

	def hide_cell(self, data, report_format):
		init_row = 3 + 10 * len(data)
		end_row = 3 + 10 * 50
		self.__select_finding_sheet()
		for row in range(init_row, end_row):
			self.current_sheet.row_dimensions[row].hidden = True
		if report_format == "QC":
			init_row_qc = 3 + 1 * len(data)
			end_row_qc = 53
			self.__select_qc_sheet()
			for row in range(init_row_qc, end_row_qc):
				self.current_sheet.row_dimensions[row].hidden = True

	def generate(self, data, project, username, report_format):
		for finding in data:
			self.__write(finding)
			self.row += 10
			if report_format == "QC":
				self.__write_qc(finding)
				self.qc_row += 1
		self.hide_cell(data, report_format)
		self.__save(project, username)


	def __select_finding_sheet(self):
		""" Seleccionar la hoja de hallazgos """
		self.current_sheet = self.workbook[
			self.sheet_names[self.lang]["finding"]
		]

	def __select_qc_sheet(self):
		""" Seleccionar la hoja de matriz qc """
		self.current_sheet = self.workbook[
			self.sheet_names[self.lang]["qc_matriz"]
		]

	def set_cell(self, col, value, inc = 0):
		""" Asigna un valor a una celda con indice Hallazgos"""
		self.current_sheet.cell(row = self.row + inc, column = col).value = value

	def set_cell_number(self, col, value, inc = 0):
		""" Asigna un valor a una celda con indice Hallazgos """
		self.current_sheet.cell(row = self.row + inc, column = col).value = float(value)

	def set_cell_qc(self, col, value, inc = 0):
		""" Asigna un valor a una celda con indice QC """
		self.current_sheet.cell(row = self.qc_row + inc, column = col).value = value

	def set_cell_number_qc(self, col, value, inc = 0):
		""" Asigna un valor a una celda con indice QC """
		self.current_sheet.cell(row = self.qc_row + inc, column = col).value = float(value)

	def __get_complexity(self, complexity_access):
		if complexity_access == "Bajo":
			return "Baja"
		elif complexity_access == "Alto":
			return "Alta"
		elif complexity_access == "Medio":
			return "Media"
		return complexity_access

	
	def __get_measure(self, metricstr): # noqa
		""" Extrae el numero de las metricas de cssv2 """
		try:
			metric = metricstr.split("|")[1]
			metric = metric.strip()
			metric = metric.split(":")[0]
			return metric.strip()
		except ValueError:
			return ""

	def __get_req(self, req_vect): # noqa
		""" Obtiene todos los identificadores con el formato REQ.XXXX """
		try:
			reqs = re.findall("REQ\\.\\d{3,4}", req_vect) # noqa
			reqs = [x.replace("REQ.", "") for x in reqs]
			reqs_list = "|".join(reqs)
			return ".*(" + reqs_list + ")"
		except ValueError:
			return ""

	def __write(self, row):
		""" Escribe un hallazgo de formstack en una fila en la hoja de Hallazgos """
		self.__select_finding_sheet()
		self.set_cell(self.finding['name'], row["hallazgo"])
		self.set_cell(self.finding['description'], row["vulnerabilidad"])
		self.set_cell(self.finding['where'], row["donde"])
		if int(row["registros_num"]) != 0:
			self.set_cell(self.finding['where_records'],
				"Evidencias/" + row["hallazgo"] + "/registros.csv")
		self.set_cell(self.finding['requirements'], row["requisitos"])
		self.set_cell_number(self.finding['criticity'], row["criticidad"])
		self.set_cell_number(self.finding['cardinality'], row["cardinalidad"])
		self.set_cell_number(self.finding['affected_records'], row["registros_num"])
		self.set_cell(self.finding['evidence'], "Evidencias/" + row["hallazgo"])
		self.set_cell(self.finding['solution'], row["solucion_efecto"])
		self.set_cell(self.finding['requirements_id'],
			self.__get_req(row["requisitos"]))
		self.set_cell(self.finding['measurements'],
			self.__get_measure(row["vector_acceso"]))
		self.set_cell(self.finding['measurements'],
			self.__get_complexity(self.__get_measure(
				row["complejidad_acceso"])),
			1)
		self.set_cell(self.finding['measurements'],
			self.__get_measure(row["autenticacion"]),
			2)
		self.set_cell(self.finding['measurements'],
			self.__get_measure(row["impacto_confidencialidad"]),
			3)
		self.set_cell(self.finding['measurements'],
			self.__get_measure(row["impacto_integridad"]),
			4)
		self.set_cell(self.finding['measurements'],
			self.__get_measure(row["impacto_disponibilidad"]),
			5)
		self.set_cell(self.finding['measurements'],
			self.__get_measure(row["explotabilidad"]),
			6)
		self.set_cell(self.finding['measurements'],
			self.__get_measure(row["nivel_resolucion"]),
			7)
		self.set_cell(self.finding['measurements'],
			self.__get_measure(row["nivel_confianza"]),
			8)

	def __write_qc(self, row):
		""" Escribe un hallazgo de formstack en una fila en la hoja de MatrizQC """
		self.__select_qc_sheet()
		self.set_cell_qc(self.matriz['type'], row["tipo_prueba"])
		self.set_cell_qc(self.matriz['component'], row["componente_aplicativo"])
		self.set_cell_qc(self.matriz['requirements_id'],
			self.__get_req(row["requisitos"]))
		self.set_cell_qc(self.matriz['requirements'], row["requisitos"])
		if "escenario" in row:
			self.set_cell_qc(self.matriz['scenario'], row["escenario"])
		if "ambito" in row:
			self.set_cell_qc(self.matriz['ambit'], row["ambito"])
		if "categoria" in row:
			self.set_cell_qc(self.matriz['category'], row["categoria"])
		if "amenaza" in row:
			self.set_cell_qc(self.matriz['threat'], row["amenaza"])
		criticity = float(row['criticidad'])
		if criticity > 6.9:
			self.set_cell_qc(self.matriz['cssv2_value'], "Alta")
		elif criticity >= 4.0:
			self.set_cell_qc(self.matriz['cssv2_value'], "Media")
		else :
			self.set_cell_qc(self.matriz['cssv2_value'], "Baja")
		if "probabilidad" in row:
			self.set_cell_qc(self.matriz['probability'], row["probabilidad"])
		if "severidad" in row:
			self.set_cell_number_qc(self.matriz['severity'], row["severidad"])
		if "riesgo" in row:
			self.set_cell_qc(self.matriz['risk'], row["riesgo"])

	def __save(self, project, username):
		self.result_filename = self.result_path
		self.result_filename += project + "_" + username + ".xlsx"
		self.workbook.save(self.result_filename)
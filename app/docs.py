# -*- coding: utf-8 -*-
"""
	Crear informe tecnico a partir de un JSON y guardarlo en formato excel
	utilizando openpyxl
	TODO: Verificar como arreglar openpyxl hay un error cuando los nombres
    de los sheet exceden 31 caracteres
"""
from openpyxl import load_workbook
from jinja2 import Environment, FileSystemLoader
from os import path
import codecs, util

config = {
    'dir': path.dirname(path.dirname(path.abspath(__file__))),
    'trim_blocks': True,
    'jinja': {
        'general': 'templates/general.txt',
        'detallado': 'templates/detallado.txt'
    },
    'xls': {
        'general': '/app/templates/fluid.xlsx',
        'detallado': '/app/templates/bancolombia.xlsx',
        'first_row': 3
    },
    'columns': {
        'fluid_hallazgos': {
            'titulo': 2,
            'vulnerabilidad': 3,
            'donde': 4,
            'requisitos': 5,
            'metricas': 7,
            'criticidad': 8,
            'cardinalidad': 9,
            'evidencia': 10,
            'solucion_efectos': 11,
            'instructivo_solucion': 12,
            'requisitos': 13,
            'amenaza':14,
            'riesgos':15
        },
        'bank_hallazgos': {
            'titulo': 2,
            'vulnerabilidad': 3,
            'donde': 4,
            'requisitos': 5,
            'metricas': 7,
            'criticidad': 8,
            'cardinalidad': 9,
            'evidencia': 10,
            'solucion_efectos': 11,
            'instructivo_solucion': 12,
            'requisitos': 13,
            'amenaza':14,
            'riesgos':15
        }
    }
}

def create_template(project_name, project_data):
    """Convierte un json en un template de jinja"""
    result_name = 'results/:name.txt'.replace(":name", project_name)
    f = codecs.open(result_name, encoding='utf-8', mode='w')
    j2 = Environment(loader = FileSystemLoader(config['dir']), trim_blocks = config['trim_blocks'])
    for i in project_data:
        if(i["tipo"] != "General"):
            f.write(j2.get_template(config['jinja']['detallado']).render(
                proyecto = project_name,
                hallazgo = "*" + i["hallazgo"].encode('ascii', 'ignore') + "*", 
                vulnerabilidad = i["vulnerabilidad"].encode('ascii', 'ignore'),
                amenaza = i["amenaza"].encode('ascii', 'ignore'),
                riesgo = i["riesgo"].encode('ascii', 'ignore'),
                donde = i["donde"].encode('ascii', 'ignore'),
                solucion = i["solucion_efecto"].encode('ascii', 'ignore') + "\n"
                )
            )
        else:
            f.write(j2.get_template(config['jinja']['general']).render(
                proyecto = project_name,
                hallazgo = "*" + i["hallazgo"].encode('ascii', 'ignore') + "*", 
                vulnerabilidad = i["vulnerabilidad"].encode('ascii', 'ignore'),
                amenaza = i["amenaza"].encode('ascii', 'ignore'),
                riesgo = i["riesgo"].encode('ascii', 'ignore'),
                donde = i["donde"].encode('ascii', 'ignore'),
                solucion = i["solucion_efecto"].encode('ascii', 'ignore') + "\n"))
    return result_name

def write_to_cell(current_sheet, row, col, value, formula=False):
    """ Asigna un valor a una celda discriminando si es de tipo formula """
    temp_cell = current_sheet.cell(row=row, column=col)
    if not formula:
        temp_cell.set_explicit_value(value=value)
    else:
        temp_cell.set_explicit_value(value=value, data_type=temp_cell.TYPE_FORMULA)

def write_number(current_sheet, row, col, value, formula=False):
    """ Asigna un valor a una celda discriminando si es de tipo formula """
    temp_cell = current_sheet.cell(row=row, column=col)
    temp_cell.value = value
    

def generate_doc_xls(project, data):
    """ Genera la documentacion xlsx de un proyecto """
    proy_type = "general"
    if "detallado" == data[0]["tipo"].lower():
        proy_type = "detallado"
    workbook_name = config['dir'] + config['xls'][proy_type]
    save_report_name = config['dir']+"/app/autodoc/results/" + project + ".xlsx"
    tech_report = load_workbook(filename=workbook_name)
    finding_sheet = tech_report["Hallazgos"]
    row = config["xls"]["first_row"]
    data = util.ord_asc_by_criticidad(data)
    for i in data:
        # Columna Titulo (2)
        write_to_cell(finding_sheet, row, 2, i["hallazgo"])
        # Columna Vulnerabilidad (3)
        write_to_cell(finding_sheet, row, 3, i["vulnerabilidad"])
        # Columna Vulnerabilidad (4)
        write_to_cell(finding_sheet, row, 4, i["donde"])
        # Columna Criticidad (8)
        write_number(finding_sheet, row, 8, float(i["criticidad"]))
        # Columna Cardinalidad (9)
        write_number(finding_sheet, row, 9, int(i["cardinalidad"]))
        # Columna Evidencia (10)
        write_to_cell(finding_sheet, row, 10, "Evidencias/" + i["hallazgo"])
        # Columna Solucion efecto (11)
        write_to_cell(finding_sheet, row, 11, i["solucion_efecto"])
        # Columna Instructivo (12)
        write_to_cell(finding_sheet, row, 12, "Soluciones/"+ i["hallazgo"])
        # Columna Ids Requisitos (13)
        write_number(finding_sheet, row, 13, ".(0144)")
        # Datos si es detallado
        if proy_type == "detallado":
            # Columna Amenaza (14)
            write_to_cell(finding_sheet, row, 14, i["amenaza"])
            # Columna Riesgo (15)
            write_to_cell(finding_sheet, row, 15, i["riesgo"])
        row = row + 10
        print i["vulnerabilidad"]
    tech_report.save(filename=save_report_name)
    """
    
    hallazgos_sheet["B3"] = "TEST HALLAZGO"
    hallazgos_sheet["C3"] = "Esto es una prueba"
    hallazgos_sheet["D3"] = "DONDE ALEX\nDONDE CHETO"
    hallazgos_sheet["M3"] = ".*(0056)"
    cell = hallazgos_sheet.cell(row=13, column=2)
    cell.set_explicit_value(value="=1+1",data_type=cell.TYPE_FORMULA)
    tech_report.save(filename = TECH_REPORT_PROJECT)
    print tech_report.sheetnames
    print "DONEEE!" 
    """

def detailed_autodoc():
    return "detailed"

def general_autodoc():
    return "general"

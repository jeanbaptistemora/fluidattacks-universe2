# -*- coding: utf-8 -*-
"""
    Procesa los parametros del front para convertirlos en un template
"""
from jinja2 import Environment, FileSystemLoader
from os import path
import codecs

config = {
    'dir': path.dirname(path.dirname(path.abspath(__file__))),
    'trim_blocks': True,
    'template': {
        'general': 'templates/general.txt',
        'detallado': 'templates/detallado.txt'
    }
}

def create_template(project_name, project_data):
    """Convierte un json en un template de jinja"""
    result_name = 'results/:name.txt'.replace(":name", project_name)
    f = codecs.open(result_name, encoding='utf-8', mode='w')
    j2 = Environment(loader = FileSystemLoader(config['dir']), trim_blocks = config['trim_blocks'])
    for i in project_data:
        if(i["tipo"] != "General"):
            f.write(j2.get_template(config['template']['detallado']).render(
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
            f.write(j2.get_template(config['template']['general']).render(
                proyecto = project_name,
                hallazgo = "*" + i["hallazgo"].encode('ascii', 'ignore') + "*", 
                vulnerabilidad = i["vulnerabilidad"].encode('ascii', 'ignore'),
                amenaza = i["amenaza"].encode('ascii', 'ignore'),
                riesgo = i["riesgo"].encode('ascii', 'ignore'),
                donde = i["donde"].encode('ascii', 'ignore'),
                solucion = i["solucion_efecto"].encode('ascii', 'ignore') + "\n"))
    return result_name
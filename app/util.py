"""Funciones de utilidad para FluidIntegrates"""

from django.http import JsonResponse
from jinja2 import Environment, FileSystemLoader
import datetime, os, codecs, time
from os import path
import re, json

def response(data, message, error):
    "Crea un objeto para enviar respuestas genericas"
    response_data = {}
    response_data['data'] = data
    response_data['message'] = message
    response_data['error'] = error
    return JsonResponse(response_data)

def traceability(msg, user):
    f = None
    BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        filename = BASE_DIR + "/logs/integrates.log"
        logmsg = str(datetime.datetime.now()) + "," + user+ "," + msg
        f = open(filename,'w')
        f.write(logmsg)
        f.close()
    except (OSError, IOError) as e:
        print "ERROR CON EL LOG " + e.message()

def is_name(name):
    """ Verifica que un parametro tenga el formato
        de nombre adecuado """
    valid = True
    try:
        if not name:
            raise ValueError("")
        elif name.strip() == "":
            raise ValueError("")
        elif not re.search("^[a-zA-Z0-9]+$",name):
            raise ValueError("")
    except ValueError:
        valid = False
    return valid

def is_json(data):
    """ Check if a param has json format"""
    valid = True
    try:
        json.loads(data)
    except ValueError:
        valid = False
    return valid

def ord_asc_by_criticidad(data):
    """ Order findings json by criticity """
    for i in range(0, len(data)-1):
        for j in range(i+1, len(data)):
            fc = float(data[i]["criticidad"])
            sc = float(data[j]["criticidad"])
            if (fc < sc):
                aux = sc
                sc = fc
                fc = aux     
    return data
 
config = {
    'dir': path.dirname(path.dirname(path.abspath(__file__))),
    'trim_blocks': True,
    'template': {
        'general': 'app/autodoc/templates/jinja.general.txt',
        'detallado': 'app/autodoc/templates/jinja.detallado.txt'
    },
    'command_path': 'app/autodoc/'
}

def create_template(project_name, project_data):
    result_name = 'app/autodoc/results/:name.adoc'.replace(":name", project_name)
    f = codecs.open(result_name, encoding='utf-8', mode='w')
    j2 = Environment(loader = FileSystemLoader(config['dir']), trim_blocks = config[    'trim_blocks'])
    for i in project_data:
        if(i["tipo"].lower() == "general"):
            f.write(j2.get_template(config['template']['general']).render(
                proyecto = project_name,
                hallazgo = "*" + i["hallazgo"].encode('ascii', 'ignore') + "*", 
                vulnerabilidad = i["vulnerabilidad"].encode('ascii', 'ignore'),
                #amenaza = i["amenaza"].encode('ascii', 'ignore'),
                #riesgo = i["riesgo"].encode('ascii', 'ignore'),
                donde = i["donde"].encode('ascii', 'ignore'),
                solucion = i["solucion_efecto"].encode('ascii', 'ignore') + "\n"))
        else:
            f.write(j2.get_template(config['template']['detallado']).render(
                proyecto = project_name,
                hallazgo = "*" + i["hallazgo"].encode('ascii', 'ignore') + "*", 
                vulnerabilidad = i["vulnerabilidad"].encode('ascii', 'ignore'),
                amenaza = i["amenaza"].encode('ascii', 'ignore'),
                riesgo = i["riesgo"].encode('ascii', 'ignore'),
                donde = i["donde"].encode('ascii', 'ignore'),
                solucion = i["solucion_efecto"].encode('ascii', 'ignore') + "\n"))
    time.sleep(5) #sleep 5 seconds, max time for generate adoc file
    command = "asciidoctor-pdf" \
        + " -a pdf-fontsdir=" + config["command_path"] + "fonts" \
        + " -a pdf-stylesdir=" + config["command_path"] + "styles" \
        + " -a pdf-style=fluid " \
        + " -o " + config["command_path"] + "results/" + project_name + ".pdf " \
        + config["command_path"] + "results/" + project_name + ".adoc"
    print command
    result = os.system(command)
    if result == 0:
        return True
    else:
        return False

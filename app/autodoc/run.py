# -*- coding: utf-8 -*-
from modules import console
from modules import formstack
from modules import jinja
from modules import commands
"""
    Description:    Flujo principal para obtener la documentacion de un proyecto
    Date:           17-08-2016
"""

project_name = console.get_project_name()
submissions = formstack.get_project(project_name)
result_file = jinja.create_template(project_name,submissions)
commands.parse_results(result_file)

# -*- coding: utf-8 -*-
"Clase para exportar los hallazgos A PDF"
import jinja2
import os
import time
import sys
import matplotlib # pylint: disable=wrong-import-position
matplotlib.use('Agg') # pylint: disable=wrong-import-position
from pylab import figure, pie, axis, legend, savefig, cla, clf, close # pylint: disable=wrong-import-position
from matplotlib.font_manager import FontProperties # pylint: disable=wrong-import-position


class CreatorPDF(object):

    STYLE_DIR = "/resources/themes"
    TPL_DIR = "/tpls/"
    FONT_DIR = "/resources/fonts"
    RESULT_DIR = "/results/"
    PROJ_TPL = "templates/executive.adoc"
    GRAPH_PATH = "/usr/src/app/app/documentator/images/"
    STYLE = "fluid"
    lang = "es"
    doctype = "executive"
    wordlist = None
    out_name = ""
    command = ""
    context = {}

    def __init__(self, lang, doctype):
        " Constructor de la clase "
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        self.RESULT_DIR = self.PATH + self.RESULT_DIR
        self.FONT_DIR = self.PATH + self.FONT_DIR
        self.TPL_DIR = self.PATH + self.TPL_DIR
        self.TPL_IMG_PATH = "/usr/src/app/app/documentator/images/"
        self.lang = lang
        self.doctype = doctype
        self.STYLE_DIR = self.PATH + self.STYLE_DIR
        if(self.doctype == "tech"):
            self.PROJ_TPL = "templates/tech.adoc"
        if(self.doctype == "presentation"):
            self.PROJ_TPL = "templates/presentation.adoc"
            self.STYLE_DIR = self.PATH + "/resources/presentation_theme"             
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.lang_support()

    def create_command(self, tpl_name):
        "Crea el comando de SO para crear el PDF con asciidoctor"
        self.command += "rm :template: &&"
        self.command = "asciidoctor-pdf "
        self.command += "-a pdf-stylesdir=:style_dir: "
        self.command += "-a pdf-style=:style: "
        self.command += "-a pdf-fontsdir=:font_dir: "
        self.command += "-D :result_dir: "
        self.command += "-o :out_name: "
        self.command += ":template: && chmod 777 :template:"
        self.command = self.command.replace(":style:", self.STYLE)
        self.command = self.command.replace(":style_dir:", self.STYLE_DIR)
        self.command = self.command.replace(":font_dir:", self.FONT_DIR)
        self.command = self.command.replace(":result_dir:", self.RESULT_DIR)
        self.command = self.command.replace(":out_name:", self.out_name)
        self.command = self.command.replace(":template:", tpl_name)

    def lang_support(self):
        self.wordlist = dict()
        self.lang_support_es()
        self.lang_support_en()

    def lang_support_es(self):
        " Agrega el diccionario de lenguaje en espanol "
        self.wordlist["es"] = {
            "finding_title": "Hallazgo",
            "finding_section_title": "Resumen de Hallazgos",
            "content_title": "Contenido",
            "content_list": [
                "1. Objetivos del Proyecto",
                "2. Tabla de Hallazgos",
                "3. Panorama General",
                "4. Resumen de Hallazgos"
            ],
            "tech": "Informe Técnico",
            "presentation": "Presentación",
            "executive": "Informe Ejecutivo",
            "goals_title": "Objetivos del proyecto",
            "metodology_title": "Metodología",
            "state_title": "Estado",
            "records_title": "Registros",
            "description_title": "Vulnerabilidad",
            "resume_vuln_title": "Vulnerabilidades",
            "where_title": "Donde",
            "resume_perc_title": "Porcentaje",
            "resume_regi_title": "Total registros comprometidos",
            "resume_vnum_title": "#",
            "resume_vname_title": "Nombre",
            "resume_ttab_title": "Tabla resumen hallazgos",
            "resume_top_title": "Top de Hallazgos",
            "threat_title": "Amenaza",
            "solution_title": "Solución",
            "requisite_title": "Requisitos",
            "treatment_title": "Tratamiento",
            "risk_title": "Riesgo",
            "evidence_title": "Evidencias",
            "compromised_system_title": "Sistema Comprometido",
            "criticity_title": "Criticidad",
            "cardinality_title": "Vulnerabilidades",
            "attack_vector_title": "Vector Ataque",
            "resume_page_title": "Panorama General",
            "resume_table_title": "Tabla de Hallazgos",
            "vuln_h": "Altos",
            "vuln_m": "Medios",
            "vuln_l": "Bajos",
            "crit_h": "(Alta)",
            "crit_m": "(Media)",
            "crit_l": "(Baja)",
            "treat_status_wor": "Pendiente",
            "treat_status_asu": "Asumido",
            "treat_status_rem": "Remediar",
        }

    def lang_support_en(self):
        " Agrega el diccionario de lenguaje en ingles "
        self.wordlist["en"] = {
            "finding_title": "Finding",
            "finding_section_title": "Finding Resume",
            "content_title": "Content",
            "content_list": [
                "1. Goals",
                "2. Finding Table",
                "3. General View",
                "4. Findings Summary"
            ],
            "tech": "Technical Report",
            "presentation": "Executive Presentation",
            "executive": "Executive Report",
            "goals_title": "Goals",
            "metodology_title": "Metodology",
            "state_title": "Status",
            "records_title": "Records",
            "description_title": "Vulnerability",
            "resume_vuln_title": "Vulnerabilities",
            "where_title": "Where",
            "resume_perc_title": "Percent",
            "resume_regi_title": "Total Records",
            "resume_vnum_title": "#",
            "resume_vname_title": "Name",
            "resume_ttab_title": "Metric Resume Table",
            "resume_top_title": "Finding Top",
            "threat_title": "Threat",
            "solution_title": "Solution",
            "requisite_title": "Requirement",
            "treatment_title": "Treatment",
            "risk_title": "Risk",
            "evidence_title": "Evidences",
            "compromised_system_title": "Compromised System",
            "criticity_title": "Criticity",
            "cardinality_title": "Vulnerabilities",
            "attack_vector_title": "Attack Vector",
            "resume_page_title": "General View",
            "resume_table_title": "Finding Table",
            "vuln_h": "High",
            "vuln_m": "Moderate",
            "vuln_l": "Low",
            "crit_h": "(High)",
            "crit_m": "(Moderate)",
            "crit_l": "(Low)",
            "treat_status_wor": "Working on it",
            "treat_status_asu": "Assumed",
            "treat_status_rem": "Remediate",
        }

    def executive(self, data, project):
        " Crea el template a renderizar y le aplica el contexto "
        self.fill_project(data, project)
        self.out_name = project + "_IE.pdf"
        searchpath = self.PATH
        template_loader = jinja2.FileSystemLoader(searchpath=searchpath)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(self.PROJ_TPL)
        tpl_name = self.TPL_DIR + ":id_IE.tpl".replace(":id", project)
        render_text = template.render(self.context)
        with open(tpl_name, "w") as tplfile:
            tplfile.write(render_text.encode("utf-8"))
        self.create_command(tpl_name)
        print self.command
        os.system(self.command)
    
    def tech(self, data, project, user):
        " Crea el template a renderizar y le aplica el contexto "
        self.fill_project(data, project)
        self.out_name = user + "_" + project + "_IT.pdf"
        searchpath = self.PATH
        template_loader = jinja2.FileSystemLoader(searchpath=searchpath)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(self.PROJ_TPL)
        tpl_name = self.TPL_DIR + ":id_IT.tpl".replace(":id", project)
        render_text = template.render(self.context)
        with open(tpl_name, "w") as tplfile:
            tplfile.write(render_text.encode("utf-8"))
        self.create_command(tpl_name)
        os.system(self.command)

    def presentation(self, data, project, project_info, user):
        " Crea el template a renderizar y le aplica el contexto "
        self.fill_project(data, project)
        self.project_info_context(project_info)
        self.out_name = user + "_" + project + "_PR.pdf"
        searchpath = self.PATH
        template_loader = jinja2.FileSystemLoader(searchpath=searchpath)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(self.PROJ_TPL)
        tpl_name = self.TPL_DIR + ":id_PR.tpl".replace(":id", project)
        render_text = template.render(self.context)
        with open(tpl_name, "w") as tplfile:
            tplfile.write(render_text.encode("utf-8"))
        self.create_command(tpl_name)
        os.system(self.command)

    def project_info_context(self, project_info):
        self.context["proyecto_fluid"] = project_info["proyecto_fluid"]
        self.context["proyecto_cliente"] = project_info["proyecto_cliente"]
        self.context["cliente"] = project_info["cliente"]
        self.context["lider"] = project_info["lider"]
        self.context["analista"] = project_info["analista"]
        self.context["arquitecto"] = project_info["arquitecto"]
        self.context["fecha_inicio"] = project_info["fecha_inicio"]
        self.context["fecha_fin"] = project_info["fecha_fin"]
        self.context["tipo_prueba"] = project_info["tipo_prueba"]
        self.context["ambiente"] = project_info["ambiente"]
        self.context["tipo_cobertura"] = project_info["tipo_cobertura"]
        self.context["mapa_hallazgos"] = project_info["mapa_hallazgos"]
        self.context["nivel_seguridad"] = project_info["nivel_seguridad"]
        self.context["cobertura"] = ""
        self.context["toe_campos_visibles"] = ""
        self.context["toe_lineas_visibles"] = ""
        self.context["toe_puertos_visibles"] = ""
        if "cobertura" in project_info:
            self.context["cobertura"] = project_info["cobertura"]
        if "toe_campos_visibles" in project_info:
            self.context["toe_campos_visibles"] = project_info["toe_campos_visibles"]
        if "toe_lineas_visibles" in project_info:
            self.context["toe_lineas_visibles"] = project_info["toe_lineas_visibles"]
        if "toe_puertos_visibles" in project_info:
            self.context["toe_puertos_visibles"] = project_info["toe_puertos_visibles"]
        self.context["toe_campos_probados"] = project_info["toe_campos_probados"]
        self.context["toe_lineas_probadas"] = project_info["toe_lineas_probadas"]
        self.context["toe_puertos_probados"] = project_info["toe_puertos_probados"]
        self.context["impacto_relevate"] = project_info["impacto_relevate"]
        self.context["observaciones"] = project_info["observaciones"]
        self.context["conclusiones"] = project_info["conclusiones"]
        self.context["recomendaciones"] = project_info["recomendaciones"]
        self.context["tipo_industria"] = project_info["tipo_industria"]
        self.context["lenguaje"] = project_info["lenguaje"]
        self.context["tipo_aplicacion"] = project_info["tipo_aplicacion"]

    def make_content(self, words):
        base = "image::../templates/:name_" + self.lang + ".png[]"
        return {
            'content_title': words['content_title'],
            'content_list': words["content_list"],
            'goals_title': words['goals_title'],
            'goals_img': base.replace(":name", "goals"),
            'criticity_img': base.replace(":name", "criticity"),
            'metodology_title': words['metodology_title'],
            'metodology_img': base.replace(":name", "metodology"),
        }

    def make_pie_finding(self, findings, project, words):
        " Crea la grafica de hallazgos "
        figure(1, figsize=(6, 6))
        finding_state_pie = [0, 0, 0]  # A, PC, C
        finding_state_pielabels = [
            words['vuln_h'],
            words['vuln_m'],
            words['vuln_l']
        ]
        colors = ["red", "orange", "yellow"]
        explode = (0, 0.1, 0)
        for finding in findings:
            criticity = float(finding["criticidad"])
            if criticity >= 7.0 and criticity <= 10:
                finding_state_pie[0] += 1
            elif criticity >= 4.0 and criticity <= 6.9:
                finding_state_pie[1] += 1
            elif criticity >= 0.0 and criticity <= 3.9:  # Abierto por defecto
                finding_state_pie[2] += 1
            else:
                finding_state_pie[2] += 1
        pie(
            finding_state_pie,
            explode=explode,
            labels=finding_state_pielabels,
            autopct='%1.0f%%',
            startangle=90,
            colors=colors
        )
        axis('equal')
        fontP = FontProperties()
        fontP.set_size('small')
        legend(prop=fontP, loc="best")
        pie_filename = 'finding_graph_:prj.png'.replace(":prj", project)
        hard_path = self.TPL_IMG_PATH
        hard_path += pie_filename
        savefig(hard_path, bbox_inches="tight", transparent=True, dpi=100)
        cla()
        clf()
        close('all')
        return pie_filename

    def make_pie_closing(self, findings, project):
        figure(1, figsize=(6, 6))
        finding_state_pie = [0, 0, 0]  # A, PC, C
        finding_state_pielabels = [
            "Abiertas",
            "Parcialmente Cerradas",
            "Cerradas"
        ]
        colors = ["red", "orange", "yellow"]
        explode = (0, 0.1, 0)
        for finding in findings:
            if finding["estado"] == "Abierto":
                finding_state_pie[0] += 1
            elif finding["estado"] == "Parcialmente cerrado":
                finding_state_pie[1] += 1
            elif finding["estado"] == "Cerrado":
                finding_state_pie[2] += 1
            else:  # Abierto por defecto
                finding_state_pie[2] += 1
        pie(
            finding_state_pie,
            explode=explode,
            labels=finding_state_pielabels,
            autopct='%1.0f%%',
            startangle=90,
            colors=colors
        )
        axis('equal')
        fontP = FontProperties()
        fontP.set_size('small')
        legend(prop=fontP, loc="best")
        pie_filename = 'main_graph_:prj.png'.replace(":prj", project)
        hard_path = self.TPL_IMG_PATH
        hard_path += pie_filename
        savefig(hard_path, bbox_inches="tight", transparent=True, dpi=100)
        cla()
        clf()
        close('all')
        return pie_filename

    def make_vuln_table(self, findings, words):
        # Label findings percent quantity
        vuln_table = [
            [words["vuln_h"], 0, 0, 0],
            [words["vuln_m"], 0, 0, 0],
            [words["vuln_l"], 0, 0, 0],
            ["Total", len(findings), "100.00%", 0],
        ]
        top_table = []
        ttl_vulns, ttl_num_reg, top = 0, 0, 1
        for finding in findings:
            criticity = float(finding["criticidad"])
            crit_as_text = words["crit_l"]
            vuln_amount = 0
            if finding['cardinalidad'] != '-':
                vuln_amount = int(finding['cardinalidad'])
            ttl_vulns += vuln_amount
            if criticity >= 7.0 and criticity <= 10:
                vuln_table[0][1] += 1
                vuln_table[0][3] += vuln_amount
                crit_as_text = words["crit_h"]
            elif criticity >= 4.0 and criticity <= 6.9:
                vuln_table[1][1] += 1
                vuln_table[1][3] += vuln_amount
                crit_as_text = words["crit_m"]
            elif criticity >= 0.0 and criticity <= 3.9:  # Abierto por defecto
                vuln_table[2][1] += 1
                vuln_table[2][3] += vuln_amount
            else:
                vuln_table[2][1] += 1
                vuln_table[2][3] += vuln_amount
            ttl_num_reg += int(finding["registros_num"])
            if top <= 5:
                top_table.append([
                    top,
                    finding["criticidad"] + " " + crit_as_text,
                    finding["hallazgo"]
                ])
                top += 1
        vuln_table[0][2] = vuln_table[0][1]*100/float(len(findings))
        vuln_table[1][2] = vuln_table[1][1]*100/float(len(findings))
        vuln_table[2][2] = vuln_table[2][1]*100/float(len(findings))
        vuln_table[0][2] = "{0:.2f}%".format(vuln_table[0][2])
        vuln_table[1][2] = "{0:.2f}%".format(vuln_table[1][2])
        vuln_table[2][2] = "{0:.2f}%".format(vuln_table[2][2])
        vuln_table[3][3] = ttl_vulns
        return {
            'resume': vuln_table,
            'top': top_table,
            'num_reg': ttl_num_reg
        }

    def fill_project(self, findings, project):
        words = self.wordlist[self.lang]
        full_project = findings[0]['proyecto_cliente']
        doctype = words[self.doctype]
        full_project += " [" + project + "]"
        team = "Engineering Team"
        version = "v1.0"
        team_mail = "engineering@fluidattacks.com"
        main_pie_filename = self.make_pie_finding(
            findings,
            project,
            words
        )
        for finding in findings:  # Fix para viejos hallazgos de formstack
            if "tratamiento" not in finding:
                finding["tratamiento"] = words["treat_status_wor"]
            elif finding["tratamiento"] == "-":
                finding["tratamiento"] = words["treat_status_wor"]
            elif finding["tratamiento"] == "Pendiente":
                finding["tratamiento"] = words["treat_status_wor"]
            elif finding["tratamiento"] == "Asumido":
                finding["tratamiento"] = words["treat_status_asu"]
            elif finding["tratamiento"] == "Remediar":
                finding["tratamiento"] = words["treat_status_rem"]
        main_pie_filename = "image::../images/" \
            + main_pie_filename \
            + '[width=330, align="center"]'
        main_tables = self.make_vuln_table(findings, words)
        fluid_tpl_content = self.make_content(words)
        self.context = {
            "full_project": full_project.upper(),
            "team": team,
            "team_mail": team_mail,
            "customer": "",
            "toe": findings[0]["proyecto_cliente"],
            "version": version,
            "revdate": doctype + " " + time.strftime("%d/%m/%Y"),
            "simpledate": time.strftime("%Y.%m.%d"),
            "fluid_tpl": fluid_tpl_content,
            "main_pie_filename": main_pie_filename,
            'main_tables': main_tables,
            "findings": findings,
            # Titulos segun lenguaje
            "finding_title": words["finding_title"],
            "finding_section_title": words["finding_section_title"],
            "where_title": words["where_title"],
            "description_title": words["description_title"],
            "resume_vuln_title": words["resume_vuln_title"],
            "resume_perc_title": words["resume_perc_title"],
            "resume_regi_title": words["resume_regi_title"],
            "resume_vnum_title": words["resume_vnum_title"],
            "resume_vname_title": words["resume_vname_title"],
            "resume_ttab_title": words["resume_ttab_title"],
            "resume_top_title": words["resume_top_title"],
            "risk_title": words["risk_title"],
            "evidence_title": words["evidence_title"],
            "records_title": words["records_title"],
            "threat_title": words["threat_title"],
            "solution_title": words["solution_title"],
            "requisite_title": words["requisite_title"],
            "treatment_title": words["treatment_title"],
            "criticity_title": words["criticity_title"],
            "cardinality_title": words["cardinality_title"],
            "attack_vector_title": words["attack_vector_title"],
            "compromised_system_title": words["compromised_system_title"],
            "resume_page_title": words["resume_page_title"],
            "resume_table_title": words["resume_table_title"],
            "state_title": words["state_title"],
            "crit_h": words["crit_h"],
            "crit_m": words["crit_m"],
            "crit_l": words["crit_l"],
        }
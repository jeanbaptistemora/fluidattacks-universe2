from pptx import Presentation

class Bancolombia:
	
    presentation = None
    critical_finding_slide = 1
    moderate_finding_slide = 10
    tolerable_finding_slide = 27
    MAX_CRITICAL_SLIDE = 10
    MAX_MODERATE_SLIDE = 27
    MAX_TOLERABLE_SLIDE = 42
    finding_positions = None
    project_name = ""
    project_data = None

    def __init__(self, project, data):
        self.project_name = project
        self.project_data = data
        self.presentation = Presentation("/var/www/fluid-integrates/app/autodoc/templates/bancolombia.pptx")
        self.finding_positions = dict()
        self.finding_positions["solucion_efecto"] = (0,0)
        self.finding_positions["riesgo"] = (1,0)
        self.finding_positions["amenaza"] = (2,0)
        self.finding_positions["vulnerabilidad"] = (3,0)
        self.finding_positions["donde"] = (4,0)
        self.finding_positions["cardinalidad"] = (6,1)
        self.finding_positions["hallazgo"] = (7,0)
        self.finding_positions["categoria"] = (7,1)
        self.finding_positions["criticidad"] = (9,1)
        self.fill_findings_table(data)
        self.fill_results_table(data)
        self.generate_doc_pptx()
		
    def get_slide(self, criticality):
        try:
            criticality = float(criticality.replace(",","."))
        except ValueError:
            criticality = 0
        except TypeError:
            criticality = 0
        if criticality == 0:
            return None
        else:
            slide = None
            if criticality > 7: #Critical
                if self.critical_finding_slide < self.MAX_CRITICAL_SLIDE:
                    slide = self.presentation.slides[self.critical_finding_slide]
                    self.critical_finding_slide = self.critical_finding_slide + 1
            elif criticality > 4 and criticality <= 6.9: #Moderated
                if self.moderate_finding_slide < self.MAX_MODERATE_SLIDE:
                    slide = self.presentation.slides[self.moderate_finding_slide]
                    self.moderate_finding_slide = self.moderate_finding_slide + 1
            else:
                if self.tolerable_finding_slide < self.MAX_TOLERABLE_SLIDE:
                    slide = self.presentation.slides[self.tolerable_finding_slide]
                    self.tolerable_finding_slide = self.tolerable_finding_slide + 1
            return slide

    def fill_findings_table(self, findings):
        # rows = 2 - 6 vulnerabilidades, cols = v.riesgo c.tecnica nombre 
        finding_table = self.presentation.slides[0].shapes[3].table
        tbl_len = len(findings)
        if len(findings) > 5:
            tbl_len = 5
        init_row = 2
        for i in range(0,tbl_len):
            # 0 = v.riesgo 1 = c.tecnica 2 = nombre 
            finding_table.rows[init_row].cells[0].text_frame.text = ""
            finding_table.rows[init_row].cells[1].text_frame.text = findings[i]["criticidad"]
            finding_table.rows[init_row].cells[2].text_frame.text = findings[i]["hallazgo"]
            init_row += 1

    def fill_results_table(self, findings):
        # rows = 1-3 hallazgos 4 total , cols = criticidad hallazgos % porcentajes
        results_table = self.presentation.slides[0].shapes[2].table
        crit = 0
        o_crit = 0
        mode = 0
        o_mode = 0
        tole = 0
        o_tole = 0
        total = len(findings)
        for finding in findings:
            criticity = finding["criticidad"]
            ocurrency = finding["cardinalidad"]
            try:
                criticity = float(criticity)
                ocurrency = float(ocurrency)
            except ValueError:
                criticity = 0
                ocurrency = 10000
            if criticity >= 7:
                crit += 1
                o_crit += ocurrency
            elif criticity >= 4 and criticity <= 6.9:
                mode += 1
                o_mode += ocurrency
            else:
                tole += 1
                o_tole += ocurrency
        #hallazgos
        results_table.rows[1].cells[1].text_frame.text = str(crit)
        results_table.rows[2].cells[1].text_frame.text = str(mode)
        results_table.rows[3].cells[1].text_frame.text = str(tole)
        results_table.rows[4].cells[1].text_frame.text = str(total)
        #Porcentaje
        results_table.rows[1].cells[2].text_frame.text = str("%.2f" % float(crit*100/float(total))) + "%"
        results_table.rows[2].cells[2].text_frame.text = str("%.2f" % float(mode*100/float(total))) + "%"
        results_table.rows[3].cells[2].text_frame.text = str("%.2f" % float(tole*100/float(total))) + "%"
        results_table.rows[4].cells[2].text_frame.text = str("%.2f" % 100.0) + "%"
        #Ocurrencias
        results_table.rows[1].cells[3].text_frame.text = str("%d" % o_crit)
        results_table.rows[2].cells[3].text_frame.text = str("%d" % o_mode)
        results_table.rows[3].cells[3].text_frame.text = str("%d" % o_tole)
        results_table.rows[4].cells[3].text_frame.text = str("%d" % int(o_crit + o_mode + o_tole))

    def fill_slide(self, finding):
        try:
            slide = self.get_slide(finding["criticidad"])
            shape, paragraph = self.finding_positions["solucion_efecto"]
            slide.shapes[shape].text_frame.paragraphs[paragraph].runs[0].text = finding["solucion_efecto"]
            shape, paragraph = self.finding_positions["riesgo"]
            slide.shapes[shape].text_frame.paragraphs[paragraph].runs[0].text = finding["riesgo"]
            shape, paragraph = self.finding_positions["amenaza"]
            slide.shapes[shape].text_frame.paragraphs[paragraph].runs[0].text = finding["amenaza"]
            shape, paragraph = self.finding_positions["vulnerabilidad"]
            slide.shapes[shape].text_frame.paragraphs[paragraph].runs[0].text = finding["vulnerabilidad"]
            shape, paragraph = self.finding_positions["donde"]
            if len(finding["donde"]) > 200:
                finding["donde"] = finding["donde"][0:200]
            finding["donde"] = finding["donde"].replace("\r", "").replace("\n","; ")
            slide.shapes[shape].text_frame.paragraphs[paragraph].runs[0].text = finding["donde"]
            shape, paragraph = self.finding_positions["cardinalidad"]
            slide.shapes[shape].text_frame.paragraphs[paragraph].runs[0].text = finding["cardinalidad"]
            shape, paragraph = self.finding_positions["hallazgo"]
            slide.shapes[shape].text_frame.paragraphs[paragraph].runs[0].text = finding["hallazgo"]
            shape, paragraph = self.finding_positions["categoria"]
            slide.shapes[shape].text_frame.paragraphs[paragraph].runs[0].text = finding["categoria"]
            shape, paragraph = self.finding_positions["criticidad"]
            slide.shapes[shape].text_frame.paragraphs[paragraph].runs[0].text = finding["criticidad"]
        except Exception, e:
            return None
		
    def generate_doc_pptx(self):
        for finding in self.project_data:
            self.fill_slide(finding)
        self.save()

    def save(self):
        self.presentation.save("/var/www/fluid-integrates/app/autodoc/results/"+ self.project_name + ".pptx")

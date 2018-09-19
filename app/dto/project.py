""" DTO to map the Integrates fields to formstack """
# pylint: disable=E0402
# Disabling this rule is necessary for importing modules beyond the top level
# pylint: disable=relative-beyond-top-level
from ..utils import forms

def parse(request_arr): # noqa: C901
    project_dict={}
    initial_dict = forms.create_dict(request_arr)
    project_fields = {
      "52601266":"fluidProject",
      "60063920":"clientProject",
      "52601817":"client",
      "52602145":"class",
      "52603216":"leader",
      "53626289":"analyst",
      "60154418":"arquitect",
      "52601351":"startDate",
      "52601570":"endDate",
      "52762210":"testType",
      "60063680":"environment",
      "60064178":"coverageType",
      "60063976":"coverage",
      "60294068":"findingsMap",
      "60294098":"securityLevel",
      "52762496":"toeVisibleFields",
      "52762572":"toeVisibleLines",
      "52762526":"toeVisiblePorts",
      "52762424":"toeTestedFields",
      "52602997":"toeTestedLines",
      "52602989":"toeTestedPorts",
      "60155980":"relevantImpact",
      "60063218":"observations",
      "60063227":"conclusions",
      "60294226":"recommendations",
      "52765044":"industryType",
      "52764314":"language",
      "52762843":"applicationType",
      "60185565":"supplies",
      "60185445":"environment_changes"
    }
    parsed_dict = {project_fields[k]:initial_dict[k] \
                   if k in initial_dict.keys() else "" \
                   for (k,v) in project_fields.items()}
    parsed_dict["timestamp"] = request_arr["timestamp"]
    project_dict["id"] = request_arr["id"]
    project_dict["data"] = parsed_dict
    return project_dict

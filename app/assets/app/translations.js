/* globals integrates,localStorage, traducciones:true, $ */
"use strict";

/**
 * @file translations.js
 * @author engineering@fluidattacks.com
 */
/**
 * Establece la configuracion de las traducciones de integrates
 * @config {AngularJS}
 * @param {Object} $translateProvider
 * @return {undefined}
 */
/** @export */
integrates.config([
  "$translateProvider",
  function ($translateProvider) {
    $translateProvider.useSanitizeValueStrategy("sanitizeParameters");
    let traducciones = {};
    let translations = {};
    translations = {
      "breadcumbs":
   {
     "eventualities": {
       "function": "Events by project",
       "page": "Events"
     },
     "findings": {
       "function": "Findings by project",
       "page": "Findings"
     }
   },
      "confirmmodal":
   {
     "confirm": "Are you sure?",
     "no": "No",
     "title_cssv2": "Update CSSv2",
     "title_description": "Update Description",
     "title_finding": "Delete Finding",
     "yes": "Yes"
   },
      "deletemodal":
   {
     "change_evidence": "Change of evidence",
     "duplicated": "It is duplicated",
     "finding_changed": "Finding has changed",
     "justification": "Justification",
     "not_vulnerability": "It is not a Vulnerability"

   },
      "event_by_name":
   {
     "btn_group": {
       "edit": "EDIT!",
       "resume": "RESUME!",
       "watch": "WATCH!"
     },
     "main_content": {
       "id": "ID",
       "name": "Name",
       "placeholder": "Name or ID project"
     },
     "modal_avance": {"title": "Events Resume"},
     "modal_edit":
        {
          "affec": "Affection",
          "analyst": "Analyst",
          "c_proj": "Customer's Project",
          "client": "Client",
          "close": "Close",
          "date": "Date",
          "detail": "Description",
          "f_proj": "FLUID's Project",
          "refresh": "Update",
          "type": "Type"
        },
     "modal_ver":
      {
        "affec": "Affection",
        "analyst": "Analyst",
        "c_proj": "Customer's Project",
        "client": "Client",
        "date": "Date",
        "detail": "Description",
        "f_proj": "FLUID's Project",
        "ok": "OK",
        "type": "Type"
      },
     "page_head": {
       "search": "Search",
       "vuln_by_proj": "Events by project "
     },
     "row":
      {
        "affect": "TOTAL AFFECTATION",
        "event": "EVENTS",
        "muted": "Please wait, loading..."
      },
     "table":
      {
        "affect": "Affectation",
        "date": "Date",
        "status": "Status",
        "type": "Type"
      }
   },
      "event_formstack":
   {
     "status": {
       "solve": "Solved",
       "unknown": "-",
       "unsolve": "Unsolved"
     },
     "type":
      {
        "approv_change": "Client approves the change of ToE",
        "auth_attack": "Authorization for special attack",
        "cancel_proj": "Client cancels the project/milestone",
        "det_attack": "Client detects an attack",
        "explic_suspend": "Client explicitly suspends project",
        "high_approval": "High availability approval",
        "inacc_ambient": "Inaccessible ambient",
        "incor_supplies": "Incorrect or missing supplies",
        "other": "other",
        "toe_differs": "ToE differs from what was approved",
        "unknown": "-",
        "uns_ambient": "Unstable ambient"
      }
   },
      "executive_report_mod":
   {
     "message": "The project's documentation has not been finished",
     "title": "Executive Reports"
   },
      "finding_formstack":
   {
     "access_vector":
      {
        "adjacent": "0.646 | Adjacent network: Exploitable from same network segment",
        "default": "-",
        "local": "0.395 | Local: Exploitable with local access to the target",
        "network": "1.000 | Network: Exploitable from Internet"
      },
     "actor":
      {
        "any_access": "Anyone with access to the station",
        "any_costumer": "Any costumer of the organization",
        "any_employee": "Any employee of the organization",
        "any_internet": "Anyone on Internet",
        "default": "-",
        "one_employee": "Only one employee",
        "some_costumer": "Only some costumers of the organization",
        "some_employee": "Only some employees"
      },
     "authentication":
      {
        "any_authen": "0.704 | None: Authentication is not required",
        "default": "-",
        "multiple_authen": "0.450 | Multiple: Multiple authentication points",
        "single_authen": "0.560 | Single: Single authentication point"
      },
     "availability":
       {
         "complete": "0.660 | Complete: There is a total target fallen",
         "default": "-",
         "none": "0 | None: There is no impact",
         "partial": "0.275 | Partial: There is intermittency in the access to the target"
       },
     "category":
        {
          "avoid_technical": "Avoid exposing the technical information of the application, servers and platforms.",
          "default": "-",
          "define_model": "Define the authorization model considering the principle of minimum privilege",
          "event": "Event",
          "exclude_data": "Exclude sensitive data from source code and event log",
          "maintain": "Maintainability",
          "performance": "Performance",
          "record_event": "Record events for traceability and audit",
          "secure_protoc": "Use secure communication protocols",
          "strengt_authen": "Strengthen controls in authentication and session management",
          "strengt_process": "Strengthen controls in file processing",
          "strengt_protect": "Strengthen the protection of stored data related to passwords or cryptographic keys",
          "update_base": "Update and configure components security baselines",
          "validate_http": "Validate the integrity of transactions in HTTP requests",
          "validate_input": "Implement controls to validate input data"
        },
     "complexity":
           {
             "default": "-",
             "high_complex": "0.350 | High: Special conditions are required like administrative access",
             "low_complex": "0.710 | Low: No special conditions are required",
             "medium_complex": "0.610 | Medium: Some conditions are required like system access"
           },
     "confidence":
       {
         "confirmed": "1.000 | Confirmed: The vulnerability is recognized by the manufacturer",
         "default": "-",
         "not_confirm": "0.900 | Not confirmed: There are few sources that recognize vulnerability",
         "not_corrob": "0.950 | Not corroborared: Vulnerability is recognized by unofficial sources"
       },
     "confidenciality":
        {
          "complete": "0.660 | Complete: Total control over information related with the target",
          "default": "-",
          "none": "0 | None: There is no impact",
          "partial": "0.275 | Partial: Access to information but no control over it"
        },
     "criticity_header": {
       "high": " High",
       "moderate": " Moderate",
       "tolerable": " Tolerable"
     },
     "exploitability":
      {
        "conceptual": "0.900 | Conceptual: There are laboratory tests",
        "default": "-",
        "functional": "0.950 | Functional: There is an exploit",
        "high": "1.000 | High: Exploit is not required or it can be automated",
        "improbable": "0.850 | Improbable: There is no exploit"
      },
     "exploitable": {
       "default": "-",
       "no": "No",
       "yes": "Yes"
     },
     "finding_type": {
       "default": "-",
       "hygiene": "Hygiene",
       "vuln": "Vulnerability"
     },
     "integrity":
      {
        "complete": "0.660 | Complete: Posibility of modify all target information",
        "default": "-",
        "none": "0 | None: There is no impact",
        "partial": "0.275 | Partial: Posibility of modify some target information"
      },
     "probability":
       {
         "default": "-",
         "diffic_vuln": "25% Difficult to have a vulnerability",
         "easy_vuln": "75% Easy to have a vulnerability",
         "possible_vuln": "50% Possible vulnerability",
         "prev_vuln": "100% previously with vulnerability"
       },
     "resolution":
       {
         "default": "-",
         "non_existent": "1.000 | Non-existent: There is no solution",
         "official": "0.870 | Official: There is an manufacturer available patch",
         "palliative": "0.950 | Palliative: There is a patch that was not published by the manufacturer",
         "temporal": "0.900 | Temporal: There are temporary solutions"
       },
     "scenario":
      {
        "anon_inter": "Anonymous from Internet",
        "anon_intra": "Anonymous from Intranet",
        "auth_inter": "Authorized Internet user",
        "auth_intra": "Authorized Intranet user",
        "default": "-",
        "infra_scan": "Infrastructure scan",
        "unauth_extra": "Unauthorized Extranet user",
        "unauth_inter": "Unauthorized Internet user"
      },
     "status":
      {
        "close": "Closed",
        "default": "-",
        "open": "Open",
        "part_close": "Partially closed"
      },
     "test_method":
      {
        "analysis": "Analysis",
        "app": "App",
        "binary": "Binary",
        "code": "Code",
        "default": "-",
        "infras": "Infrastructure"
      },
     "treatment_header":
      {
        "asummed": "Asummed",
        "default": "-",
        "remediated": "Remediate",
        "working": "Working on it"
      }
   },
      "forms":
   {
     "closure": "Closure",
     "events": "Events",
     "findings": "Findings",
     "progress": "Progress"
   },
      "grapExploit":
   {
     "exploit_label": "Exploitable",
     "nonexploit_label": "Not Exploitable",
     "title": "Exploitability"
   },
      "grapStatus":
   {
     "close_label": "Closed",
     "open_label": "Open",
     "partial_label": "Partial",
     "title": "Findings by Status"
   },
      "grapType":
   {
     "hig_label": "Hygiene",
     "seg_label": "Vulnerability",
     "title": "Finding Type"
   },
      "left_menu": {
        "first": "Findings",
        "second": "Events",
        "third": "Forms"
      },
      "logout":
   {
     "cancel": "Cancel",
     "message": "Are you sure?",
     "ok": "Logout",
     "title": "Close Session"
   },
      "main_content":
   {
     "eventualities":
      {
        "close": "CLOSE",
        "date": "Date",
        "description": "Description",
        "description_1": "You can check the details of an event by ",
        "description_2": "clicking",
        "description_3": "on it",
        "project_title": "FLUID's Project",
        "title": "My Events",
        "type": "Type"
      },
     "projects":
      {
        "description1": "You can check the details of a project by ",
        "description2": "clicking",
        "description3": " on it",
        "project_description": "Description",
        "project_title": "FLUID's Project",
        "title": "My Projects"
      }
   },
      "progress_mod": {
        "finding": "Finding",
        "title": "Progress Report"
      },
      "proj_alerts":
   {
     "access_denied": "Access Denied",
     "attent_cont": "Empty search",
     "attent_title": "Attention!",
     "congratulation": "Congratulations",
     "differ_comment": "You must enter a new treatment justification",
     "empty_comment": "You must enter a treatment justification!",
     "error_severity": "Severity must be an integer bewteen 0 and 5",
     "error_text": "There is an error",
     "error_textsad": "There is an error :(",
     "event_exist": "This proyect has no vulnerabilities or does not exist",
     "event_formstack": "Unable to access Formstack",
     "event_internal": "Internal error, loading...",
     "event_positiveint": "Affectation must be a positive integer or zero",
     "event_required": "Name or ID is required",
     "event_select": "You must select an event",
     "event_title": "Searching",
     "event_updated": "Event updated",
     "event_wait": "Wait a moment please...",
     "file_size": "The file size must be less than 10mb",
     "file_size_png": "The image size must be less than 2mb",
     "file_size_py": "The file size must be less than 1mb",
     "file_type_csv": "The file must be .csv type",
     "file_type_gif": "The image must be .gif type",
     "file_type_png": "The image must be .png type",
     "file_type_py": "The file must be .py type",
     "no_file_update": "Failed to update the file",
     "no_finding": "We could not find the finding!",
     "no_text_update": "Failed to update the description",
     "not_found": "We could not find it!",
     "project_deleted": "Project Deleted",
     "remediated_success": "This finding was marked as remediated. A request to verify the solution was sent",
     "search_cont": "Searching Project...",
     "search_title": "News!",
     "short_comment": "You must enter a justification of at least 50 characters and maximum 80 characters",
     "short_remediated_comment": "You must enter a justification of at least 100 characters",
     "updated_cont": "Updated ;)",
     "updated_cont_description": "Description Updated ;)",
     "updated_cont_file": "File Updated ;)",
     "updated_title": "Correct!",
     "updated_treat": "Treatment updated",
     "verified_success": "This finding was marked as verified.",
     "wrong_severity": "You must calculate severity correctly"
   },
      "registration":
   {
     "close_modal": "Are you sure?",
     "close_session": "Close Session",
     "hello": "Hello",
     "no": "No",
     "no_authorization": "You do not have authorization for login yet. Please contact FLUID's staff to get access.",
     "yes": "Yes"
   },
      "search_findings":
   {
     "descriptions":
      {
        "description1": "",
        "description2": "Click",
        "description3": "on a finding to see more details"
      },
     "event_table": {
       "date": "Date",
       "id": "ID",
       "status": "Status",
       "type": "Type"
     },
     "eventualities": {"description": "Click on an event to see more details"},
     "filter_buttons": {
       "advance": "Progress",
       "documentation": "Documentation"
     },
     "filter_labels":
      {
        "cardinalities": "Open Vulnerabilities",
        "closure": "Fixed vulnerabilities",
        "criticity": "Total Severity Found",
        "findings": "Findings"
      },
     "filter_menu": {
       "search": {
         "button": "Search",
         "placeholder": "FLUID project name"
       }
     },
     "page_head": {"breadcrumb": {"project": "Project"}},
     "pop_table":
      {
        "date": "Date",
        "details": "Description",
        "status": "Status",
        "type": "Type"
      },
     "project_buttons": {
       "back": "Back",
       "delete": "Delete"
     },
     "project_labels":
      {
        "client": "Customer's Project",
        "criticity": "Severity",
        "project": "FLUID's Project",
        "report": "Report Date",
        "status": "Status",
        "type": "Type",
        "vulnerabilities": "Open Vulnerabilities"
      },
     "tab_comments": {"comments_name": "Comments"},
     "tab_cssv2":
        {
          "authentication": "Authentication",
          "availability": "Availability Impact",
          "complexity": "Access Complexity",
          "confidence": "Confidence Level",
          "confidenciality": "Confidentiality Impact",
          "description_name": "Severity",
          "editable": "Edit",
          "exploitability": "Exploitability",
          "integrity": "Integrity Impact",
          "resolution": "Resolution Level",
          "update": "Update",
          "vector": "Access Vector"
        },
     "tab_description":
       {
         "bts_external": "BTS External",
         "cardinality": "Open Vulnerabilities",
         "category": "Category",
         "description": "Description",
         "description_name": "Description",
         "detailed": "Detailed",
         "edit_treatment": "Edit",
         "editable": "Edit",
         "general": "General",
         "probability": "Probability",
         "recommendation": "Recommendation",
         "records": "Compromised Records",
         "remediated": "Request Verification",
         "remediated_finding": "Finding remediated",
         "requirements": "Requirements",
         "risk": "Risk Value",
         "severity": "Severity",
         "solution": "Applied Solution Justification",
         "stage": "Scenario",
         "system": "Affected Systems",
         "threat": "Threat",
         "title": "Title",
         "totalrecords": "Total Compromised Records",
         "treat_justification": "Treatment Justification",
         "treat_manager": "Treatment Manager",
         "treatment": "Treatment",
         "type": "Finding Type",
         "update": "Update",
         "update_treatment": "Update",
         "update_treatmodal": "Update Treatment",
         "vectors": "Attack Vectors",
         "verified": "Verified",
         "verified_finding": "Finding verified",
         "weakness": "Weakness",
         "where": "Where"
       },
     "tab_evidence":
         {
           "alert": "In progress...",
           "animation_exploit": "Exploitation animation",
           "detail": "Detail",
           "editable": "Edit",
           "evidence_exploit": "Exploitation evidence",
           "evidence_name": "Evidence",
           "update": "Update"
         },
     "tab_records": {"records_name": "Records"},
     "tab_tracking":
       {
         "cicle": "Closing cycle",
         "close": "Closed Vulnerabilities",
         "finding": "Discovery",
         "open": "Open Vulnerabilities"
       },
     "table": {
       "headings": {
         "action": "Action",
         "age": "Age (Days)",
         "cardinality": "Open Vuln.",
         "criticity": "Severity",
         "exploit": "Exploitable",
         "finding": "Title",
         "state": "Status",
         "timestamp": "Date",
         "treatment": "Treatment",
         "type": "Type",
         "vulnerability": "Description"
       }
     }
   },
      "tab_container": {
        "eventualities": "Events",
        "findings": "Findings",
        "metrics": "Metrics"
      },
      "technical_report_mod":
      {
        "body_1": "Technical report is protected by password. The password is the date of  report's PDF generation and your username.",
        "body_2": "Example: someone@fluidattacks.com generates the technical report on 03/15/2018 therefore, the password is 15032018someone",
        "title": "Technical Reports"
      }
    };
    traducciones = {
      "breadcumbs":
   {
     "eventualities":
      {
        "function": "Eventualidades por proyecto",
        "page": "Eventualidades"
      },
     "findings": {
       "function": "Hallazgos por proyecto",
       "page": "Hallazgos"
     }
   },
      "confirmmodal":
   {
     "confirm": "¿Realizar esta acción?",
     "no": "Cancelar",
     "title_cssv2": "Actualizar CSSv2",
     "title_description": "Actualizar Descripción",
     "title_finding": "Eliminar Hallazgo",
     "yes": "Aceptar"
   },
      "deletemodal":
   {
     "change_evidence": "Cambio de Evidencia",
     "duplicated": "Está Duplicado",
     "finding_changed": "Por Modificación del Hallazgo",
     "justification": "Justificación",
     "not_vulnerability": "No es una Vulnerabilidad"
   },
      "event_by_name":
   {
     "btn_group": {
       "edit": "EDITAR!",
       "resume": "RESUMEN!",
       "watch": "VER!"
     },
     "main_content":
      {
        "id": "ID",
        "name": "Nombre",
        "placeholder": "Nombre o ID de proyecto"
      },
     "modal_avance": {"title": "Resumen eventualidades"},
     "modal_edit":
      {
        "affec": "Afectacion",
        "analyst": "Analista",
        "c_proj": "Proyecto Cliente",
        "client": "Cliente",
        "date": "Fecha",
        "detail": "Detalle",
        "f_proj": "Proyecto FLUID",
        "ok": "OK",
        "type": "Tipo"
      },
     "modal_ver":
      {
        "affec": "Afectacion",
        "analyst": "Analista",
        "c_proj": "Proyecto Cliente",
        "client": "Cliente",
        "close": "Cerrar",
        "date": "Fecha",
        "detail": "Detalle",
        "f_proj": "Proyecto FLUID",
        "refresh": "Actualizar",
        "type": "Tipo"
      },
     "page_head":
       {
         "search": "Busqueda",
         "vuln_by_proj": "Eventualidades por proyecto"
       },
     "row":
      {
        "affect": "AFECTACION TOTAL",
        "event": "EVENTUALIDADES",
        "muted": "Un momento por favor, cargando..."
      },
     "table":
      {
        "affect": "Afectacion",
        "date": "Fecha",
        "status": "Estado",
        "type": "Tipo"
      }

   },
      "event_formstack":
   {
     "status": {
       "solve": "Tratada",
       "unknown": "-",
       "unsolve": "Pendiente"
     },
     "type":
      {
        "approv_change": "Cliente aprueba cambio de alcance",
        "auth_attack": "Autorización para ataque especial",
        "cancel_proj": "Cliente cancela el proyecto/hito",
        "det_attack": "Cliente detecta ataque",
        "explic_suspend": "Cliente suspende explicitamente",
        "high_approval": "Aprobación de alta disponibilidad",
        "inacc_ambient": "Ambiente no accesible",
        "incor_supplies": "Insumos incorrectos o faltantes",
        "other": "Otro",
        "toe_differs": "Alcance difiere a lo aprobado",
        "unknown": "-",
        "uns_ambient": "Ambiente inestable"
      }
   },
      "executive_report_mod":
   {
     "message": "La documentación del proyecto no ha sido finalizada",
     "title": "Informes Ejecutivos"
   },
      "finding_formstack":
   {
     "access_vector":
      {
        "adjacent": "0.646 | Red adyacente: Explotable desde el mismo segmento de red",
        "default": "-",
        "local": "0.395 | Local: Explotable con acceso local al objetivo",
        "network": "1.000 | Red: Explotable desde Internet"
      },
     "actor":
      {
        "any_access": "Cualquier persona con acceso a la estación",
        "any_costumer": "Cualquier cliente de la organización",
        "any_employee": "Cualquier empleado de la organización",
        "any_internet": "Cualquier persona en Internet",
        "default": "-",
        "one_employee": "Solo un empleado",
        "some_costume": "Solo algunos clientes de la organización",
        "some_employee": "Solo algunos empleados"
      },
     "authentication":
      {
        "any_authen": "0.704 | Ninguna: No se requiere autenticación",
        "default": "-",
        "multiple_authen": "0.450 | Multiple: Multiples puntos de autenticación",
        "single_authen": "0.560 | Única: Único punto de autenticación"
      },
     "availability":
       {
         "complete": "0.660 | Completo: Hay una caída total del objetivo",
         "default": "-",
         "none": "0 | Ninguno: No se presenta ningún impacto",
         "partial": "0.275 | Parcial: Se presenta intermitencia en el acceso al objetivo"
       },
     "category":
        {
          "avoid_technical": "Evitar exponer la información técnica de la aplicación, servidores y plataformas",
          "default": "-",
          "define_model": "Definir el modelo de autorización considerando el principio de mínimo privilegio",
          "event": "Eventualidad",
          "exclude_data": "Excluir datos sensibles del código fuente y del registro de eventos",
          "maintain": "Mantenibilidad",
          "performance": "Desempeño",
          "record_event": "Registrar eventos para trazabilidad y auditoría",
          "secure_protoc": "Utilizar protocolos de comunicación seguros",
          "strengt_authen": "Fortalecer controles en autenticación y manejo de sesión",
          "strengt_process": "Fortalecer controles en el procesamiento de archivos",
          "strengt_protect": "Fortalecer la protección de datos almacenados relacionados con contraseñas o llaves criptográficas",
          "update_base": "Actualizar y configurar las líneas base de seguridad de los componentes",
          "validate_http": "Validar la integridad de las transacciones en peticiones HTTP",
          "validate_input": "Implementar controles para validar datos de entrada"
        },
     "complexity":
        {
          "default": "-",
          "high_complex": "0.350 | Alto: Se requieren condiciones especiales como acceso administrativo",
          "low_complex": "0.710 | Bajo: No se requiere ninguna condición especial",
          "medium_complex": "0.610 | Medio: Se requieren algunas condiciones como acceso al sistema"
        },
     "confidence":
         {
           "confirmed": "1.000 | Confirmado: La vulnerabilidad es reconocida por el fabricante",
           "default": "-",
           "not_confirm": "0.900 | No confirmado: Existen pocas fuentes que reconocen la vulnerabilidad",
           "not_corrob": "0.950 | No corroborado: La vulnerabilidad es reconocida por fuentes no oficiales"
         },
     "confidenciality":
      {
        "complete": "0.660 | Completo: Se controla toda la información relacionada con el objetivo",
        "default": "-",
        "none": "0 | Ninguno: No se presenta ningún impacto",
        "partial": "0.275 | Parcial: Se obtiene acceso a la información pero no control sobre ella"
      },
     "criticity_header": {
       "high": " Alto",
       "moderate": " Moderado",
       "tolerable": " Tolerable"
     },
     "exploitability":
       {
         "conceptual": "0.900 | Conceptual: Existen pruebas de laboratorio",
         "default": "-",
         "functional": "0.950 | Funcional: Existe exploit",
         "high": "1.000 | Alta: No se requiere exploit o se puede automatizar",
         "improbable": "0.850 | Improbable: No existe un exploit"
       },
     "exploitable": {
       "default": "-",
       "no": "No",
       "yes": "Si"
     },
     "finding_type": {
       "default": "-",
       "hygiene": "Higiene",
       "vuln": "Vulnerabilidad"
     },
     "integrity":
      {
        "complete": "0.660 | Completo: Es posible modificar toda la información del objetivo",
        "default": "-",
        "none": "0 | Ninguno: No se presenta ningún impacto",
        "partial": "0.275 | Parcial: Es posible modificar cierta información del objetivo"
      },
     "probability":
       {
         "default": "-",
         "diffic_vuln": "25% Difícil de vulnerar",
         "easy_vuln": "75% Fácil de vulnerar",
         "possible_vuln": "50% Posible de vulnerar",
         "prev_vuln": "100% Vulnerado Anteriormente"
       },
     "resolution":
      {
        "default": "-",
        "non_existent": "1.000 | Inexistente: No existe solución",
        "official": "0.870 | Oficial: Existe un parche disponible por el fabricante",
        "palliative": "0.950 | Paliativa: Existe un parche que no fue publicado por el fabricante",
        "temporal": "0.900 | Temporal: Existen soluciones temporales"
      },
     "scenario":
       {
         "anon_inter": "Anónimo desde Internet",
         "anon_intra": "Anónimo desde Intranet",
         "auth_inter": "Internet usuario autorizado",
         "auth_intra": "Intranet usuario autorizado",
         "default": "-",
         "infra_scan": "Escaneo de Infraestructura",
         "unauth_extra": "Extranet usuario no autorizado",
         "unauth_inter": "Internet usuario no autorizado"
       },
     "status":
       {
         "close": "Cerrado",
         "default": "-",
         "open": "Abierto",
         "part_close": "Parcialmente cerrado"
       },
     "test_method":
      {
        "analysis": "Análisis",
        "app": "Aplicación",
        "binary": "Binario",
        "code": "Código",
        "default": "-",
        "infras": "Infraestructura"
      },
     "treatment_header":
      {
        "asummed": "Asumido",
        "default": "-",
        "remediated": "Remediar",
        "working": "Pendiente"
      }
   },
      "forms":
   {
     "closure": "Cierre",
     "events": "Eventualidades",
     "findings": "Hallazgos",
     "progress": "Avance"
   },
      "grapExploit":
   {
     "exploit_label": "Explotable",
     "nonexploit_label": "No Explotable",
     "title": "Distribucion por Explotabilidad"
   },
      "grapStatus":
   {
     "close_label": "Cerrados",
     "open_label": "Abiertos",
     "partial_label": "Parciales",
     "title": "Hallazgos por Estado"
   },
      "grapType":
   {
     "hig_label": "Higiene",
     "seg_label": "Vulnerabilidad",
     "title": "Distribucion por Tipo Hallazgo"
   },
      "left_menu":
   {
     "first": "Hallazgos",
     "second": "Eventualidades",
     "third": "Formularios"
   },
      "logout":
   {
     "cancel": "Cancelar",
     "message": "Esta seguro de que desea salir?",
     "ok": "Salir",
     "title": "Cerrar Sesión"
   },
      "main_content":
   {
     "eventualities":
      {
        "close": "CERRAR",
        "date": "Fecha",
        "description": "Detalle",
        "description_1": "Para ver el detalle de la eventualidad debes hacer",
        "description_2": "click",
        "description_3": "sobre la eventualidad",
        "project_title": "Proyecto FLUID",
        "title": "Mis Eventualidades",
        "type": "Tipo"
      },
     "projects":
      {
        "description1": "Para ver el detalle del proyecto debes hacer ",
        "description2": "click",
        "description3": " sobre el proyecto",
        "project_description": "Descripción",
        "project_title": "Proyecto FLUID",
        "title": "Mis Proyectos"
      }
   },
      "progress_mod": {
        "finding": "Hallazgo",
        "title": "Reporte de Avance"
      },
      "proj_alerts":
   {
     "access_denied": "Acceso Denegado",
     "attent_cont": "Busqueda vacia",
     "attent_title": "Cuidado!",
     "congratulation": "Felicidades",
     "differ_comment": "Debes ingresar una nueva justificación del tratamiento",
     "empty_comment": "Debes ingresar una justificación del tratamiento!",
     "error_severity": "La severidad debe ser un numero de 0 a 5",
     "error_text": "Hay un error",
     "error_textsad": "Hay un error :(",
     "event_exist": "Este proyecto no tiene eventualidades o no existe",
     "event_formstack": "No se tuvo acceso a Formstack...",
     "event_internal": "Error interno, cargando datos...",
     "event_positiveint": "La afectación debe ser un número positivo o cero",
     "event_required": "El nombre es obligatorio",
     "event_select": "Debes seleccionar una eventualidad",
     "event_title": "Consultando",
     "event_updated": "Eventualidad actualizada",
     "event_wait": "Un momento por favor...",
     "file_size": "El archivo debe tener un tamaño menor a 10mb",
     "file_size_png": "La imagen debe tener un tamaño menor a 2mb",
     "file_size_py": "El archivo debe tener un tamaño menor a 1mb",
     "file_type_csv": "El archivo debe ser de tipo .csv",
     "file_type_gif": "La imagen debe ser de tipo .gif",
     "file_type_png": "La imagen debe ser de tipo .png",
     "file_type_py": "El archivo debe ser de tipo .py",
     "no_file_update": "Falló al actualizar el archivo",
     "no_finding": "No encontramos el hallazgo!",
     "no_text_update": "Falló al actualizar la descripción",
     "not_found": "No pudimos encontrarlo!",
     "project_deleted": "Projecto Eliminado",
     "remediated_success": "El hallazgo fue marcado como remediado, la solicitud de revisión de la solución fue enviada",
     "search_cont": "Buscando Proyecto...",
     "search_title": "Noticia!",
     "short_comment": "Debes ingresar una justificación de mínimo 50 caracteres y máximo 80 caracteres",
     "short_remediated_comment": "Debes ingresar una justificación de mínimo 100 caracteres",
     "updated_cont": "Actualizado ;)",
     "updated_cont_description": "Descripción Actualizada ;)",
     "updated_cont_file": "Archivo Actualizado ;)",
     "updated_title": "Correcto!",
     "updated_treat": "El tratamiento fue actualizado",
     "verified_success": "El hallazgo fue marcado como remediado.",
     "wrong_severity": "Debes calcular correctamente la severidad"
   },
      "registration":
   {
     "close_modal": "Esta seguro de que desea salir?",
     "close_session": "Cerrar Sesión",
     "hello": "Hola",
     "no": "No",
     "no_authorization": "No tienes autorización aún para ingresar. Comunícate con un representante de FLUID para obtener acceso.",
     "yes": "Si"
   },
      "search_findings":
   {
     "descriptions":
      {
        "description1": "Haz",
        "description2": "click",
        "description3": "para ver mas detalles del hallazgo"
      },
     "event_table": {
       "date": "Fecha",
       "id": "ID",
       "status": "Estado",
       "type": "Tipo"
     },
     "eventualities": {"description": "Haz click para ver el detalle"},
     "filter_buttons": {
       "advance": "Avance",
       "documentation": "Documentacion"
     },
     "filter_labels":
      {
        "cardinalities": "Vulnerabilidades Abiertas",
        "closure": "Vulnerabilidades remediadas",
        "criticity": "Criticidad Total Encontrada",
        "findings": "Hallazgos"
      },
     "filter_menu": {
       "search": {
         "button": "Ejecutar esta busqueda",
         "placeholder": "Nombre del proyecto en FLUID"
       }
     },
     "page_head": {"breadcrumb": {"project": "Proyecto"}},
     "pop_table":
      {
        "date": "Fecha",
        "details": "Descripcion",
        "status": "Estado",
        "type": "Tipo"
      },
     "project_buttons": {
       "back": "Volver",
       "delete": "Eliminar"
     },
     "project_labels":
      {
        "client": "Proyecto Cliente",
        "criticity": "Criticidad",
        "project": "Proyecto FLUID",
        "report": "Fecha Reporte",
        "status": "Estado",
        "type": "Tipo",
        "vulnerabilities": "Vulnerabilidades Abiertas"
      },
     "tab_comments": {"comments_name": "Comentarios"},
     "tab_cssv2":
       {
         "authentication": "Autenticacion",
         "availability": "Impacto Disponibilidad",
         "complexity": "Complejidad Acceso",
         "confidence": "Nivel Confianza",
         "confidenciality": "Impacto Confidencialidad",
         "description_name": "Severidad",
         "editable": "Editar",
         "exploitability": "Explotabilidad",
         "integrity": "Impacto Integridad",
         "resolution": "Nivel Resolucion",
         "update": "Actualizar",
         "vector": "Vector de Acceso"
       },
     "tab_description":
      {
        "bts_external": "BTS Externo",
        "cardinality": "Vulnerabilidades Abiertas",
        "category": "Categoria",
        "description": "Descripcion",
        "description_name": "Descripcion",
        "detailed": "Detallado",
        "edit_treatment": "Editar",
        "editable": "Editar",
        "general": "General",
        "probability": "Probabilidad",
        "recommendation": "Recomendacion",
        "records": "Registros Comprometidos",
        "remediated": "Solicitar Verificación",
        "remediated_finding": "Hallazgo remediado",
        "requirements": "Requisitos",
        "risk": "Valor Riesgo",
        "severity": "Severidad",
        "solution": "Justificación de la Solución Aplicada",
        "stage": "Escenario",
        "system": "Sistemas Comprometidos",
        "threat": "Amenaza",
        "title": "Titulo",
        "totalrecords": "Total Registros Comprometidos",
        "treat_justification": "Justificación del Tratamiento",
        "treat_manager": "Responsable del Tratamiento",
        "treatment": "Tratamiento",
        "type": "Tipo Hallazgo",
        "update": "Actualizar",
        "update_treatment": "Actualizar",
        "update_treatmodal": "Actualizar Tratamiento",
        "vectors": "Vectores de ataque",
        "verified": "Verificado",
        "verified_finding": "Hallazgo verificado",
        "weakness": "Debilidad",
        "where": "Donde"
      },
     "tab_evidence":
      {
        "alert": "En desarrollo...",
        "animation_exploit": "Animación de explotación",
        "detail": "Detalle",
        "editable": "Editar",
        "evidence_exploit": "Evidencia de explotación",
        "evidence_name": "Evidencia",
        "update": "Actualizar"
      },
     "tab_records": {"records_name": "Registros"},
     "tab_tracking":
      {
        "cicle": "Ciclo de cierre",
        "close": "Vulnerabilidades Cerradas",
        "finding": "Hallazgo reportado",
        "open": "Vulnerabilidades Abiertas"
      },
     "table": {
       "headings": {
         "action": "Accion",
         "age": "Edad (Días)",
         "cardinality": "Vuln. Abiertas",
         "criticity": "Severidad",
         "exploit": "Explotable",
         "finding": "Titulo",
         "state": "Estado",
         "timestamp": "Fecha",
         "treatment": "Tratamiento",
         "type": "Tipo",
         "vulnerability": "Descripcion"
       }
     }
   },
      "tab_container": {
        "eventualities": "Eventualidades",
        "findings": "Hallazgos",
        "metrics": "Métricas"
      },
      "technical_report_mod":
   {
     "body_1": "El reporte técnico está protegido por contraseña. La contraseña es la fecha del día de generación del informe y su nombre de usuario.",
     "body_2": "Ejemplo: alguien@fluidattacks.com genera el reporte técnico en la fecha 15/03/2018 por lo tanto, la contraseña es 15032018alguien",
     "title": "Informes Técnicos"
   }
    };
    if (typeof localStorage.lang === "undefined") {
      localStorage.lang = "en";
    }
    $translateProvider.
      translations("en", translations).
      translations("es", traducciones).
      preferredLanguage(localStorage.lang);
  }
]);

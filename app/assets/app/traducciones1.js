/*
 * This file does not allow exports or globals.
 */
/* eslint-disable no-unused-vars */
const traducciones1 = {
  "finding_formstack":
{
  "exploitable": {
    "default": "-",
    "no": "No",
    "yes": "Si"
  },
  "findingType": {
    "default": "-",
    "hygiene": "Higiene",
    "security": "Seguridad"
  },
  "integrity":
  {
    "complete": "0.660 | Completo: Es posible modificar toda la " +
                "información del objetivo",
    "default": "-",
    "none": "0 | Ninguno: No se presenta ningún impacto",
    "partial": "0.275 | Parcial: Es posible modificar cierta " +
               "información del objetivo"
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
    "official": "0.870 | Oficial: Existe un parche disponible " +
                "por el fabricante",
    "palliative": "0.950 | Paliativa: Existe un parche que no fue " +
                  "publicado por el fabricante",
    "temporal": "0.900 | Temporal: Existen soluciones temporales"
  },
  "scenario":
   {
     "anon_inter": "Anónimo desde Internet",
     "anon_intra": "Anónimo desde Intranet",
     "auth_extra": "Usuario de Extranet autorizado",
     "auth_inter": "Usuario de Internet autorizado",
     "auth_intra": "Usuario de Intranet autorizado",
     "default": "-",
     "infra_scan": "Escaneo de Infraestructura",
     "unauth_extra": "Usuario de Extranet no autorizado",
     "unauth_inter": "Usuario de Internet no autorizado",
     "unauth_intra": "Usuario de Intranet no autorizado"
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
    "accepted": "Asumido",
    "default": "-",
    "remediated": "Remediar",
    "working": "Nuevo"
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
  "exploit_label": "Si",
  "nonexploit_label": "No",
  "title": "Explotabilidad"
},
  "grapStatus":
{
  "close_label": "Cerrados",
  "open_label": "Abiertos",
  "partial_label": "Parciales",
  "title": "Estado"
},
  "grapType":
{
  "hig_label": "Higiene",
  "seg_label": "Seguridad",
  "title": "Tipo"
},
  "left_menu":
{
  "first": "Proyectos",
  "third": "Formularios"
},
  "legalNotice":
{
  "acceptBtn":
  {
    "text": "Aceptar y continuar",
    "tooltip": "Haz click si entiendes y aceptas los términos anteriores"
  },
  "description": "Integrates, Copyright (c) 2019 Fluid Attacks. " +
  "Esta plataforma contiene información de propiedad de Fluid Attacks. " +
  "Dicha información puede ser usada por el cliente sólo con el propósito " +
  "de documentación sin poder divulgar su contenido " +
  "a terceras partes ya que contiene ideas, conceptos, precios y/o " +
  "estructuras de propiedad de Fluid Attacks. La clasificación " +
  "'propietaria' significa que esta información es solo para uso de las " +
  "personas a quienes está dirigida. En caso de requerirse copias totales " +
  "o parciales se debe contar con la autorización expresa y escrita de " +
  "Fluid Attacks. Las normas que fundamentan la clasificación de " +
  "la información son los artículos 72 y siguientes de la decisión del " +
  "acuerdo de Cartagena, 344 de 1.993, el artículo 238 del código " +
  "penal y los artículos 16 y siguientes de la ley 256 de 1.996.",
  "rememberCbo":
  {
    "text": "Recordar mi decisión",
    "tooltip": "Marca la casilla si prefieres que esta decisión sea permanente"
  },
  "title": "Aviso legal"
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
    "descPluralAlert1": "Existen ",
    "descPluralAlert2": "eventualidades abiertas que comprometen el adecuado " +
                    "desempeño del proyecto, por favor darle el adecuado " +
                    "tratamiento.",
    "descSingularAlert1": "Atención! ",
    "descSingularAlert2": "Existe ",
    "descSingularAlert3": "eventualidad abierta que compromete el " +
                          "adecuado desempeño del proyecto, por " +
                          "favor darle el adecuado tratamiento."
  },
  "projects":
  {
    "description1": "Para ver el detalle del proyecto debes hacer ",
    "description2": "click",
    "description3": " sobre el proyecto",
    "project_description": "Descripción",
    "project_title": "Proyecto Fluid",
    "title": "Mis Proyectos"
  }
},
  "progress_mod": {
    "finding": "Hallazgo",
    "title": "Reporte de Avance"
  },
  "proj_alerts":
{
  "access_denied": "Acceso denegado o projecto no encontrado",
  "attentTitle": "Cuidado!",
  "attent_cont": "Busqueda vacia",
  "congratulation": "Felicidades",
  "differ_comment": "Debes ingresar una nueva justificación del tratamiento",
  "emptyField": "Debes ingresar una afectación",
  "empty_comment": "Debes ingresar una justificación del tratamiento!",
  "errorUpdatingEvent": "Ocurrió un error actualizando la eventualidad",
  "error_severity": "La severidad debe ser un numero de 0 a 5",
  "error_text": "Hay un error",
  "error_textsad": "Hay un error :(",
  "eventExist": "Este proyecto no tiene eventualidades",
  "eventFormstack": "No se tuvo acceso a Formstack...",
  "eventPositiveint": "La afectación debe ser un número positivo o cero",
  "eventUpdated": "Eventualidad actualizada",
  "file_size": "El archivo debe tener un tamaño menor a 10mb",
  "file_size_png": "La imagen debe tener un tamaño menor a 2mb",
  "file_size_py": "El archivo debe tener un tamaño menor a 1mb",
  "file_type_csv": "El archivo debe ser de tipo .csv",
  "file_type_gif": "La imagen debe ser de tipo .gif",
  "file_type_png": "La imagen debe ser de tipo .png",
  "file_type_py": "El archivo debe ser de tipo .py",
  "file_type_wrong": "El archivo tiene un formato desconocido o no permitido",
  "file_type_yaml": "El archivo debe ser de tipo .yaml o .yml",
  "invalid_schema": "El archivo no cumple con el esquema",
  "no_file_update": "Falló al actualizar el archivo",
  "no_finding": "No encontramos el hallazgo!",
  "no_text_update": "Falló al actualizar la descripción",
  "project_deleted": "Projecto Eliminado",
  "range_error": "Los límites del rango son incorrectos",
  "remediated_success": "El hallazgo fue marcado como remediado, la " +
                       "solicitud de revisión de la solución fue enviada",
  "short_comment": "Debes ingresar una justificación de mínimo 30 " +
                  "caracteres",
  "short_remediated_comment": "Debes ingresar una justificación de " +
                             "mínimo 100 caracteres",
  "updatedTitle": "Correcto!",
  "updated_cont": "Actualizado ;)",
  "updated_cont_description": "Descripción Actualizada ;)",
  "updated_cont_file": "Archivo Actualizado ;)",
  "updated_treat": "El tratamiento fue actualizado",
  "verified_success": "El hallazgo fue marcado como remediado.",
  "wrong_severity": "Debes calcular correctamente la severidad"
},
  "registration": {
    "continue_btn": "Continuar como",
    "greeting": "Hola",
    "logged_in_message": "Por favor ciérrala antes de intentar " +
                          "acceder con otra cuenta",
    "logged_in_title": "Ya has iniciado sesión",
    "not_authorized": "Aún no tienes autorización para ingresar. " +
                      "Por favor contacta al personal de Fluid o a tu " +
                      "administrador de proyecto para obtener acceso."
  },
  "reports":
{
  "executive_report_mod":
  {
    "message": "La documentación del proyecto no ha sido finalizada",
    "title": "Informes Ejecutivos"
  },
  "technical_report_mod":
  {
    "body_1": "El informe técnico está protegido por contraseña. " +
              "La contraseña es la fecha del día de generación del " +
              "informe y su nombre de usuario.",
    "body_2": "Ejemplo: alguien@fluidattacks.com genera el informe " +
              "técnico en la fecha 15/03/2018 por lo tanto, la " +
              "contraseña es 15032018alguien",
    "title": "Informes Técnicos"
  },
  "title": "Informes"
}
};

/*
 * This file does not allow exports or globals.
 */
/* eslint-disable no-unused-vars */
const traducciones1 = {
  "confirmmodal":
{
  "accept_draft": "Aceptar Draft",
  "cancel": "Cancelar",
  "confirm": "¿Realizar esta acción?",
  "delete_draft": "Eliminar Draft",
  "no": "Cancelar",
  "proceed": "Proceder",
  "title_cssv2": "Actualizar CSSv2",
  "title_description": "Actualizar Descripción",
  "title_finding": "Eliminar Hallazgo",
  "title_project": "Eliminar Proyecto",
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
  "eventFormstack":
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
  "event_by_name":
{
  "btn_group": {
    "edit": "EDITAR!",
    "resume": "RESUMEN!",
    "watch": "VER!"
  },
  "modal_avance": {"title": "Resumen eventualidades"},
  "modal_edit":
  {
    "close": "Cerrar",
    "refresh": "Actualizar"
  },
  "modal_ver":
  {
    "accessibility": "Eventualidad presente en",
    "affec": "Afectación",
    "affec_components": "Insumos afectados",
    "analyst": "Analista",
    "c_proj": "Proyecto Cliente",
    "client": "Cliente",
    "close": "Cerrar",
    "date": "Fecha",
    "detail": "Detalle",
    "f_proj": "Proyecto FLUID",
    "refresh": "Actualizar",
    "type": "Tipo"
  }
},
  "finding_formstack":
{
  "access_vector":
  {
    "adjacent": "0.646 | Red adyacente: Explotable desde el " +
                "mismo segmento de red",
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
    "multiple_authen": "0.450 | Multiple: Multiples " +
                       "puntos de autenticación",
    "single_authen": "0.560 | Única: Único punto de autenticación"
  },
  "availability":
   {
     "complete": "0.660 | Completo: Hay una caída total del objetivo",
     "default": "-",
     "none": "0 | Ninguno: No se presenta ningún impacto",
     "partial": "0.275 | Parcial: Se presenta intermitencia en el " +
                "acceso al objetivo"
   },
  "category":
    {
      "avoid_technical": "Evitar exponer la información técnica de la " +
                         "aplicación, servidores y plataformas",
      "default": "-",
      "define_model": "Definir el modelo de autorización considerando el " +
                      "principio de mínimo privilegio",
      "event": "Eventualidad",
      "exclude_data": "Excluir datos sensibles del código fuente y " +
                      "del registro de eventos",
      "maintain": "Mantenibilidad",
      "performance": "Desempeño",
      "record_event": "Registrar eventos para trazabilidad y auditoría",
      "secure_protoc": "Utilizar protocolos de comunicación seguros",
      "strengt_authen": "Fortalecer controles en autenticación y " +
                        "manejo de sesión",
      "strengt_process": "Fortalecer controles en el " +
                         "procesamiento de archivos",
      "strengt_protect": "Fortalecer la protección de datos " +
                         "almacenados relacionados con contraseñas " +
                         "o llaves criptográficas",
      "update_base": "Actualizar y configurar las líneas base de " +
                     "seguridad de los componentes",
      "validate_http": "Validar la integridad de las transacciones en " +
                       "peticiones HTTP",
      "validate_input": "Implementar controles para validar " +
                        "datos de entrada"
    },
  "complexity":
    {
      "default": "-",
      "high_complex": "0.350 | Alto: Se requieren condiciones " +
                      "especiales como acceso administrativo",
      "low_complex": "0.710 | Bajo: No se requiere ninguna " +
                     "condición especial",
      "medium_complex": "0.610 | Medio: Se requieren algunas " +
                        "condiciones como acceso al sistema"
    },
  "confidence":
     {
       "confirmed": "1.000 | Confirmado: La vulnerabilidad es " +
                    "reconocida por el fabricante",
       "default": "-",
       "not_confirm": "0.900 | No confirmado: Existen pocas " +
                      "fuentes que reconocen la vulnerabilidad",
       "not_corrob": "0.950 | No corroborado: La vulnerabilidad es " +
                     "reconocida por fuentes no oficiales"
     },
  "confidenciality":
  {
    "complete": "0.660 | Completo: Se controla toda la información " +
                "relacionada con el objetivo",
    "default": "-",
    "none": "0 | Ninguno: No se presenta ningún impacto",
    "partial": "0.275 | Parcial: Se obtiene acceso a la información " +
               "pero no control sobre ella"
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
  "findingType": {
    "default": "-",
    "hygiene": "Higiene",
    "vuln": "Vulnerabilidad"
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
  "seg_label": "Vulnerabilidad",
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
  "description": "Integrates, Copyright (c) 2018 FLUID. Esta plataforma " +
  "contiene información de propiedad de Fluidsignal Group. " +
  "Dicha información puede ser usada por el cliente sólo con el propósito " +
  "de documentación sin poder divulgar su contenido " +
  "a terceras partes ya que contiene ideas, conceptos, precios y/o " +
  "estructuras de propiedad de Fluidsignal Group S.A. La clasificación " +
  "'propietaria' significa que esta información es solo para uso de las " +
  "personas a quienes está dirigida. En caso de requerirse copias totales " +
  "o parciales se debe contar con la autorización expresa y escrita de " +
  "Fluidsignal Group S.A. Las normas que fundamentan la clasificación de " +
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
  "search_cont": "Buscando Proyecto...",
  "search_title": "Noticia!",
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
                      "Por favor contacta al personal de FLUID o a tu " +
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

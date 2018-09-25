/*
 * This file does not allow exports or globals.
 */
/* eslint-disable no-unused-vars */
const traducciones2 = {
  "search_events": {
    "headings": {
      "date": "Date",
      "details": "Description",
      "id": "ID",
      "status": "Status",
      "type": "Type"
    }
  },
  "search_findings":
{
  "environment_table": {"environment": "Ambiente"},
  "filter_labels":
  {
    "cardinalities": "Vulnerabilidades Abiertas",
    "cardinalitiesTooltip": "Vulnerabilidades pendientes por solución",
    "closure": "Vulnerabilidades remediadas",
    "closureTooltip": "Porcentaje de vulnerabilidades reportadas " +
                      "que han sido solucionadas",
    "compromisedRecords": "Total Registros Comprometidos",
    "compromisedRecordsTooltip": "Total de los registros comprometidos " +
                                 "presentes en el proyecto",
    "criticity": "Criticidad Total Encontrada",
    "criticityTooltip": "Criticidad del proyecto comparado con la media " +
                        "(<100% más seguro, >100% más inseguro)",
    "findings": "Hallazgos",
    "findingsTooltip": "Vulnerabilidades de seguridad reportadas por categoría",
    "maximumSeverity": "Máxima Severidad Encontrada",
    "maximumSeverityTooltip": "Máxima severidad encontrada de acuerdo " +
                              "al estándar CVSS",
    "oldestFinding": "Día(s) del Hallazgo Abierto más Antiguo",
    "oldestFindingTooltip": "Edad de la vulnerabilidad abierta con más " +
                            "días desde su reporte",
    "openEvents": "Eventualidades Abiertas",
    "openEventsTooltip": "Eventos que impiden el normal desarrollo " +
                          "del proyecto",
    "vulnerabilities": "Vulnerabilidades Totales",
    "vulnerabilitiesTooltip": "Total de vulnerabilidades reportadas"
  },
  "filter_menu": {
    "search": {
      "button": "Ejecutar esta busqueda",
      "placeholder": "Nombre del proyecto en FLUID"
    }
  },
  "headings": {
    "action": "Accion",
    "age": "Edad (Días)",
    "cardinality": "Vuln. Abiertas",
    "criticity": "Severidad",
    "exploit": "Explotable",
    "finding": "Titulo",
    "lastVulnerability": "Último Reporte (Días)",
    "released": "Liberado",
    "state": "Estado",
    "timestamp": "Fecha",
    "treatment": "Tratamiento",
    "type": "Tipo",
    "vulnerability": "Descripcion"
  },
  "page_head": {"breadcrumb": {"project": "Proyecto"}},
  "pop_table":
  {
    "date": "Fecha",
    "details": "Descripción",
    "status": "Estado",
    "type": "Tipo"
  },
  "project_buttons": {
    "accept": "Aceptar",
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
  "repositories_table": {
    "branch": "Rama",
    "repository": "Repositorio"
  },
  "tab_comments": {"comments_name": "Comentarios"},
  "tab_cssv2":
   {
     "authentication": "Autenticación",
     "availability": "Impacto Disponibilidad",
     "complexity": "Complejidad Acceso",
     "confidence": "Nivel Confianza",
     "confidenciality": "Impacto Confidencialidad",
     "description_name": "Severidad",
     "editable": "Editar",
     "exploitability": "Explotabilidad",
     "integrity": "Impacto Integridad",
     "resolution": "Nivel Resolución",
     "update": "Actualizar",
     "vector": "Vector de Acceso"
   },
  "tab_description":
  {
    "actorTooltip": "Persona que podría ejecutar el vector de ataque, que " +
                    "afecta a los activos especificados, usando el hallazgo",
    "btsTooltip": "Link a un sistema de seguimiento de errores externo",
    "bts_external": "BTS Externo",
    "cardinality": "Vulnerabilidades Abiertas",
    "category": "Categoria",
    "compromisedAtributes": "Atributos Comprometidos",
    "compromisedAtributesTooltip": "Atributos que fueron comprometidos al " +
                                    "explotar la vulnerabilidad",
    "compromisedRecords": "Registros Comprometidos",
    "compromisedRecordsTooltip": "Número de datos comprometidos al explotar " +
                                  "la vulnerabilidad",
    "description": "Descripción",
    "descriptionTooltip": "Descripción del hallazgo",
    "description_name": "Descripción",
    "detailed": "Detallado",
    "edit_treatment": "Editar",
    "editable": "Editar",
    "general": "General",
    "probability": "Probabilidad",
    "recommendation": "Recomendación",
    "recommendationTooltip": "Recomendación general que se da para evitar " +
                              "esta falla de seguridad",
    "remediated": "Solicitar Verificación",
    "remediated_finding": "Hallazgo remediado",
    "requirements": "Requisitos",
    "requirementsTooltip": "Requisito del criterio de seguridad inclumplido " +
                            "por el cual se está materializando el riesgo",
    "risk": "Valor Riesgo",
    "severity": "Severidad",
    "solution": "Justificación de la Solución Aplicada",
    "stage": "Escenario",
    "stageTooltip": "Lugar desde donde se explota la vulnerabilidad",
    "system": "Sistemas Comprometidos",
    "systemTooltip": "Nombre de los sistemas que fueron afectados al " +
                      "explotar este hallazgo",
    "threat": "Amenaza",
    "threatTooltip": "Descripción de la amenaza que representa la presencia " +
                      "de esta falla de seguridad",
    "title": "Titulo",
    "treat_justification": "Justificación del Tratamiento",
    "treat_justificationTooltip": "Justificación del tratamiento dado al " +
                                  "hallazgo",
    "treat_manager": "Responsable del Tratamiento",
    "treat_managerTooltip": "Persona que definió o modificó el tratamiento " +
                            "que se dará",
    "treatment": "Tratamiento",
    "treatmentTooltip": "Tratamiento que se le dará al hallazgo",
    "type": "Tipo Hallazgo",
    "update": "Actualizar",
    "update_treatment": "Actualizar",
    "update_treatmodal": "Actualizar Tratamiento",
    "vectors": "Vectores de ataque",
    "vectorsTooltip": "Descripción del caso de abuso generado por este " +
                      " hallazgo",
    "verified": "Verificado",
    "verified_finding": "Hallazgo verificado",
    "weakness": "Debilidad",
    "weaknessTooltip": "Link de la vulnerabilidad categorizada en la CWE",
    "where": "Donde",
    "whereTooltip": "URL y/o puertos de los recursos que tienen " +
                    "vulnerabilidades de seguridad"
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
  "tab_observations": {"observations_name": "Observaciones"},
  "tab_records": {"records_name": "Registros"},
  "tab_resources":
  {
    "add_repository": "Agregar",
    "branch": "Rama",
    "environment": "Ambiente",
    "environments": "Ambientes",
    "no_selection": "Debe seleccionar un item de la tabla.",
    "password": "Contraseña",
    "remove_repository": "Remover",
    "repeated_item": "Uno o varios items a añadir ya existen.",
    "repositories": "Repositorios",
    "repository": "Repositorio",
    "success": "Item agregado exitosamente.",
    "success_remove": "Item eliminado exitosamente.",
    "title_env": "Agregar información de los ambientes",
    "title_repo": "Agregar información de los repositorios",
    "username": "Usuario"
  },
  "tab_tracking":
  {
    "cicle": "Ciclo",
    "close": "Cerradas",
    "closingEffectiveness": "Efectividad",
    "finding": "Hallazgo reportado",
    "open": "Abiertas",
    "tracking_name": "Seguimiento"
  },
  "tab_users": {
    "add_button": "Agregar",
    "admin": "Admin",
    "analyst": "Analista",
    "assign_error": "Sólo puedes agregar a un administrador a la vez.",
    "customer": "Usuario",
    "customer_admin": "Manager",
    "days_ago": " dia(s) atrás",
    "developer": "Desarrollador",
    "edit": "Edit",
    "edit_user_title": "Editar información del usuario",
    "email": "alguien@dominio.com",
    "email_title": "Email",
    "error_phone": "El número telefónico no debe contener letras o " +
                    "caracteres especiales",
    "hours_ago": " hora(s) atrás",
    "minutes_ago": " minuto(s) atrás",
    "months_ago": " mes(es) atrás",
    "no_selection": "Debe seleccionar un correo de la tabla.",
    "phone_number": "Número Telefónico",
    "remove_admin": "Remover admin",
    "remove_admin_error": "Sólo puedes remover a un administrador a la vez.",
    "remove_user": "Remover",
    "requiered_field": "Este campo es requerido.",
    "responsibility_placeholder": "Product Owner, Gerente del " +
                                  "proyecto, Tester, ...",
    "role": "Rol",
    "success": " fue agregado a este proyecto exitosamente.",
    "success_admin": "Información de usuario actualizada.",
    "success_admin_remove": " ya no es administrador de este proyecto.",
    "success_delete": " fue removido del proyecto.",
    "textbox": "Ingresa el correo de la persona que deseas agregar, este " +
                "debe ser un correo de Office 365 o Google.",
    "title": "Agregar usuario a este proyecto",
    "title_success": "Felicitaciones",
    "undefined": "-",
    "user_max_responsibility": "Debes ingresar una responsabilidad de máximo " +
                                "50 caracteres",
    "user_organization": "Organización",
    "user_responsibility": "Responsabilidad",
    "wrong_format": "El correo ingresado no es valido."
  },
  "users_table": {
    "firstlogin": "Primer ingreso",
    "lastlogin": "Último ingreso",
    "phoneNumber": "Número Telefónico",
    "userOrganization": "Organización",
    "userResponsibility": "Responsabilidad",
    "userRole": "Rol",
    "usermail": "Email"
  }
},
  "tab_container": {
    "eventualities": "Eventualidades",
    "findings": "Hallazgos",
    "indicators": "Indicadores",
    "resources": "Insumos",
    "users": "Usuarios"
  }
};

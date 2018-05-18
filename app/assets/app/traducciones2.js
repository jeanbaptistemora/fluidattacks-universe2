/*
 * This file does not allow exports or globals.
 */
/* eslint-disable no-unused-vars */
const traducciones2 = {
  "search_findings":
{
  "filter_labels":
  {
    "cardinalities": "Vulnerabilidades Abiertas",
    "cardinalitiesTooltip": "Vulnerabilidades pendientes por solución",
    "closure": "Vulnerabilidades remediadas",
    "closureTooltip": "Porcentaje de vulnerabilidades reportadas " +
                      "que han sido solucionadas",
    "criticity": "Criticidad Total Encontrada",
    "criticityTooltip": "Criticidad del proyecto comparado con la media " +
                        "(<100% más seguro, >100% más inseguro)",
    "findings": "Hallazgos",
    "findingsTooltip": "Vulnerabilidades de seguridad reportadas por categoría",
    "maximumSeverity": "Máxima Severidad Encontrada",
    "maximumSeverityTooltip": "Máxima severidad encontrada de acuerdo " +
                              "al estándar CVSS",
    "oldestFinding": "Hallazgo con Mayor Edad",
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
    "description": "Descripcion",
    "descriptionTooltip": "Descripción del hallazgo",
    "description_name": "Descripcion",
    "detailed": "Detallado",
    "edit_treatment": "Editar",
    "editable": "Editar",
    "general": "General",
    "probability": "Probabilidad",
    "recommendation": "Recomendacion",
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
  "tab_records": {"records_name": "Registros"},
  "tab_tracking":
  {
    "cicle": "Ciclo",
    "close": "Cerradas",
    "closingEffectiveness": "Efectividad",
    "finding": "Hallazgo reportado",
    "open": "Abiertas"
  }
},
  "tab_container": {
    "eventualities": "Eventualidades",
    "findings": "Hallazgos",
    "indicators": "Indicadores"
  }
};

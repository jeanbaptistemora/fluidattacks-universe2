/* tslint:disable max-line-length
 *  Disabling for the sake of readability of this association between formstack values and translation strings
 */

export const translationsMap: { [fsValue: string]: string } = {
  "Alta: No se requiere exploit o se puede automatizar": "search_findings.tab_severity.exploitability_options.high",
  "Alto: Se requieren condiciones especiales como acceso administrativo": "search_findings.tab_severity.complexity_options.high_complex",
  "Bajo: No se requiere ninguna condición especial": "search_findings.tab_severity.complexity_options.low_complex",
  "Completo: Es posible modificar toda la información del objetivo": "search_findings.tab_severity.integrity_options.complete",
  "Completo: Hay una caída total del objetivo": "search_findings.tab_severity.availability_options.complete",
  "Completo: Se controla toda la información relacionada con el objetivo": "search_findings.tab_severity.confidentiality_options.complete",
  "Conceptual: Existen pruebas de laboratorio": "search_findings.tab_severity.exploitability_options.conceptual",
  "Confirmado: La vulnerabilidad es reconocida por el fabricante": "search_findings.tab_severity.confidence_options.confirmed",
  "Funcional: Existe exploit": "search_findings.tab_severity.exploitability_options.functional",
  "Improbable: No existe un exploit": "search_findings.tab_severity.exploitability_options.improbable",
  "Inexistente: No existe solución": "search_findings.tab_severity.resolution_options.non_existent",
  "Local: Explotable con acceso local al objetivo": "search_findings.tab_severity.vector_options.local",
  "Medio: Se requieren algunas condiciones como acceso al sistema": "search_findings.tab_severity.complexity_options.medium_complex",
  "Multiple: Multiples puntos de autenticación": "search_findings.tab_severity.authentication_options.multiple_auth",
  "Ninguna: No se requiere autenticación": "search_findings.tab_severity.authentication_options.no_auth",
  "Ninguno: No se presenta ningún impacto": "search_findings.tab_severity.availability_options.none",
  "No confirmado: Existen pocas fuentes que reconocen la vulnerabilidad": "search_findings.tab_severity.confidence_options.not_confirm",
  "No corroborado: La vulnerabilidad es reconocida por fuentes no oficiales": "search_findings.tab_severity.confidence_options.not_corrob",
  "Oficial: Existe un parche disponible por el fabricante": "search_findings.tab_severity.resolution_options.official",
  "Paliativa: Existe un parche que no fue publicado por el fabricante": "search_findings.tab_severity.resolution_options.palliative",
  "Parcial: Es posible modificar cierta información del objetivo": "search_findings.tab_severity.integrity_options.partial",
  "Parcial: Se obtiene acceso a la información pero no control sobre ella": "search_findings.tab_severity.confidentiality_options.partial",
  "Parcial: Se presenta intermitencia en el acceso al objetivo": "search_findings.tab_severity.availability_options.partial",
  "Red adyacente: Explotable desde el mismo segmento de red": "search_findings.tab_severity.vector_options.adjacent",
  "Red: Explotable desde Internet": "search_findings.tab_severity.vector_options.network",
  "Temporal: Existen soluciones temporales": "search_findings.tab_severity.resolution_options.temporal",
  "Única: Único punto de autenticación": "search_findings.tab_severity.authentication_options.single_auth",
};

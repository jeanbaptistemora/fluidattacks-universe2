/* eslint-disable max-len */
/*
 * This file does not allow exports or globals.
 */
/* eslint-disable no-unused-vars */
const fieldsToTranslate = [
  "actor",
  "authentication",
  "category",
  "accessComplexity",
  "scenario",
  "estado",
  "exploitability",
  "exploitable",
  "confidentialityImpact",
  "availabilityImpact",
  "integrityImpact",
  "confidenceLevel",
  "resolutionLevel",
  "probability",
  "clientFindingType",
  "testType",
  "accessVector",
  "treatment",
  "releaseStatus"
];
const eventsTranslations = [
  "eventType",
  "eventStatus"
];
const keysToTranslate = {
  "100% Vulnerado Anteriormente": "finding_formstack.probability.prev_vuln",
  "25% Difícil de vulnerar": "finding_formstack.probability.diffic_vuln",
  "50% Posible de vulnerar": "finding_formstack.probability.possible_vuln",
  "75% Fácil de vulnerar": "finding_formstack.probability.easy_vuln",
  "ANALYSIS": "finding_formstack.test_method.analysis",
  "APP": "finding_formstack.test_method.app",
  "Abierto": "finding_formstack.status.open",
  "Actualizar y configurar las líneas base de seguridad de los componentes": "finding_formstack.category.update_base",
  "Ambiente inestable": "eventFormstack.type.uns_ambient",
  "Ambiente no accesible": "eventFormstack.type.inacc_ambient",
  "Anónimo desde Internet": "finding_formstack.scenario.anon_inter",
  "Anónimo desde Intranet": "finding_formstack.scenario.anon_intra",
  "Asumido": "finding_formstack.treatment_header.asummed",
  "BINARY": "finding_formstack.test_method.binary",
  "Cerrado": "finding_formstack.status.close",
  "Cualquier cliente de la organización": "finding_formstack.actor.any_costumer",
  "Cualquier empleado de la organización": "finding_formstack.actor.any_employee",
  "Cualquier persona con acceso a la estación": "finding_formstack.actor.any_access",
  "Definir el modelo de autorización considerando el principio de mínimo privilegio": "finding_formstack.category.define_model",
  "Desempeño": "finding_formstack.category.performance",
  "Escaneo de Infraestructura": "finding_formstack.scenario.infra_scan",
  "Eventualidad": "finding_formstack.category.event",
  "Evitar exponer la información técnica de la aplicación, servidores y plataformas": "finding_formstack.category.avoid_technical",
  "Excluir datos sensibles del código fuente y del registro de eventos": "finding_formstack.category.exclude_finding",
  "Fortalecer controles en autenticación y manejo de sesión": "finding_formstack.category.strengt_authen",
  "Fortalecer controles en el procesamiento de archivos": "finding_formstack.category.strengt_process",
  "Fortalecer la protección de datos almacenados relacionados con contraseñas o llaves criptográficas": "finding_formstack.category.strengt_protect",
  "Higiene": "finding_formstack.findingType.hygiene",
  "INFRASTRUCTURE": "finding_formstack.test_method.infras",
  "Implementar controles para validar datos de entrada": "finding_formstack.category.validate_input",
  "Mantenibilidad": "finding_formstack.category.maintain",
  "No": "finding_formstack.exploitable.no",
  "Nuevo": "finding_formstack.treatment_header.working",
  "Parcialmente cerrado": "finding_formstack.status.part_close",
  "Registrar eventos para trazabilidad y auditoría": "finding_formstack.category.record_event",
  "Remediar": "finding_formstack.treatment_header.remediated",
  "SOURCE_CODE": "finding_formstack.test_method.code",
  "Si": "finding_formstack.exploitable.yes",
  "Solo algunos clientes de la organización": "finding_formstack.actor.some_costumer",
  "Solo algunos empleados": "finding_formstack.actor.some_employee",
  "Solo un empleado": "finding_formstack.actor.one_employee",
  "Usuario de Extranet no autorizado": "finding_formstack.scenario.unauth_extra",
  "Usuario de Internet autorizado": "finding_formstack.scenario.auth_inter",
  "Usuario de Internet no autorizado": "finding_formstack.scenario.unauth_inter",
  "Usuario de Intranet autorizado": "finding_formstack.scenario.auth_intra",
  "Usuario de Intranet no autorizado": "finding_formstack.scenario.unauth_intra",
  "Utilizar protocolos de comunicación seguros": "finding_formstack.category.secure_protoc",
  "Validar la integridad de las transacciones en peticiones HTTP": "finding_formstack.category.validate_http",
  "Vulnerabilidad": "finding_formstack.findingType.vuln",
  "authorization_special_attack": "eventFormstack.type.auth_attack",
  "client_approves_change_toe": "eventFormstack.type.approv_change",
  "client_cancels_project_milestone": "eventFormstack.type.cancel_proj",
  "client_detects_attack": "eventFormstack.type.det_attack",
  "client_explicitly_suspends_project": "eventFormstack.type.explic_suspend",
  "high_availability_approval": "eventFormstack.type.high_approval",
  "incorrect_missing_supplies": "eventFormstack.type.incor_supplies",
  "other": "eventFormstack.type.other",
  "solved": "eventFormstack.status.solve",
  "toe_differs_approved": "eventFormstack.type.toe_differs",
  "unsolved": "eventFormstack.status.unsolve",
  "​Cualquier persona en Internet": "finding_formstack.actor.any_internet"
};

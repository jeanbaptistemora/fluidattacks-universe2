const esTranslations: Map<string, string> = {
  confirmmodal: {
    cancel: "Cancelar",
    message: "¿Está seguro?",
    proceed: "Proceder",
    title_cvssv2: "Actualizar CVSSv2",
    title_generic: "Confirmar acción",
  },
  legalNotice: {
    acceptBtn: {
      text: "Aceptar y continuar",
      tooltip: "Haz click si entiendes y aceptas los términos anteriores",
    },
    description: "Integrates, Copyright (c) 2019 Fluid Attacks. Esta plataforma \
    contiene información de propiedad de Fluid Attacks. Dicha información \
    puede ser usada por el cliente sólo con el propósito de documentación sin \
    poder divulgar su contenido a terceras partes ya que contiene ideas, \
    conceptos, precios y/o estructuras de propiedad de Fluid Attacks. \
    La clasificación 'propietaria' significa que esta información es solo para \
    uso de las personas a quienes está dirigida. En caso de requerirse copias \
    totales o parciales se debe contar con la autorización expresa y escrita de \
    Fluid Attacks. Las normas que fundamentan la clasificación de la \
    información son los artículos 72 y siguientes de la decisión del acuerdo de \
    Cartagena, 344 de 1.993, el artículo 238 del código penal y los artículos \
    16 y siguientes de la ley 256 de 1.996.",
    rememberCbo: {
      text: "Recordar mi decisión",
      tooltip: "Marca la casilla si prefieres que esta decisión sea permanente",
    },
    title: "Aviso legal",
  },
  proj_alerts: {
    access_denied: "Acceso denegado o proyecto no encontrado",
    error_textsad: "Hay un error :(",
    file_size: "El archivo debe tener un tamaño menor a 10mb",
    file_size_png: "La imagen debe tener un tamaño menor a 2mb",
    file_size_py: "El archivo debe tener un tamaño menor a 1mb",
    file_type_csv: "El archivo debe ser de tipo .csv",
    file_type_gif: "La imagen debe ser de tipo .gif",
    file_type_png: "La imagen debe ser de tipo .png",
    file_type_py: "El archivo debe ser de tipo .py",
    file_type_wrong: "El archivo tiene un formato desconocido o no permitido",
    file_type_yaml: "El archivo debe ser de tipo .yaml o .yml",
    file_updated: "Archivo Actualizado ;)",
    invalid_schema: "El archivo no cumple con el esquema",
    invalid_treatment_mgr: "Por favor seleccione un responsable del tratamiento",
    no_file_selected: "No se ha seleccionado ningún archivo",
    no_file_update: "Falló al actualizar el archivo",
    range_error: "Los límites del rango son incorrectos",
    title_success: "Felicitaciones",
    updated: "Actualizado",
    updated_title: "Correcto!",
    verified_success: "El hallazgo fue marcado como remediado.",
  },
  registration: {
    continue_btn: "Continuar como",
    greeting: "¡Hola",
    logged_in_message: "Por favor ciérrala antes de intentar acceder con otra cuenta.",
    logged_in_title: "Ya has iniciado sesión",
    unauthorized: "Aún no tienes autorización para ingresar. Por favor contacta al personal de Fluid Attacks o a tu " +
      "administrador de proyecto para obtener acceso.",
  },
  search_findings: {
    environment_table: {
      environment: "Ambiente",
    },
    files_table: {
      description: "Descripción",
      file: "Archivo",
      upload_date: "Fecha",
    },
    repositories_table: {
      branch: "Rama",
      repository: "URL Repositorio",
    },
    tab_comments: {
      tab_title: "Comentarios",
    },
    tab_description: {
      action: "Acción",
      actor: {
        any_costumer: "Cualquier cliente de la organización",
        any_employee: "Cualquier empleado de la organización",
        any_internet: "Cualquier persona en Internet",
        any_station: "Cualquier persona con acceso a la estación",
        one_employee: "Solo un empleado",
        some_costumer: "Solo algunos clientes de la organización",
        some_employee: "Solo algunos empleados",
        title: "Actor",
      },
      affected_systems: "Sistemas comprometidos",
      ambit: {
        applications: "Aplicaciones",
        databases: "Bases de datos",
        infra: "Infraestructura",
        sourcecode: "Código fuente",
        title: "Ámbito",
      },
      attack_vectors: "Vectores de ataque",
      bts: "BTS Externo",
      category: {
        define_auth_model: "Definir el modelo de autorización considerando el principio de mínimo privilegio",
        event: "Eventualidad",
        expose_tech_info: "Evitar exponer la información técnica de la aplicación, servidores y plataformas",
        http_req_integrity: "Validar la integridad de las transacciones en peticiones HTTP",
        log_events: "Registrar eventos para trazabilidad y auditoría",
        maintainability: "Mantenibilidad",
        performance: "Desempeño",
        secure_protocols: "Utilizar protocolos de comunicación seguros",
        sensible_data_code: "Excluir datos sensibles del código fuente y del registro de eventos",
        strengthen_auth_session: "Fortalecer controles en autenticación y manejo de sesión",
        strengthen_file_processing: "Fortalecer controles en el procesamiento de archivos",
        strengthen_password_keys: "Fortalecer la protección de datos almacenados relacionados con contraseñas o llaves \
                                   criptográficas",
        title: "Categoría",
        update_sec_baselines: "Actualizar y configurar las líneas base de seguridad de los componentes",
        validate_input: "Implementar controles para validar datos de entrada",
      },
      compromised_attrs: "Atributos comprometidos",
      compromised_records: "Registros comprometidos",
      customer_project_code: "Código en el cliente",
      customer_project_name: "Nombre en el cliente",
      description: "Descripción",
      download_vulnerabilities: "Descargar Vulnerabilidades",
      editable: "Editar",
      errorFileVuln: "El archivo de vulnerabilidades tiene errores",
      field: "Campo",
      inputs: "Entradas",
      kb: "URL solución",
      line: "Línea",
      line_plural: "Líneas",
      mark_verified: "Verificar",
      path: "Ruta",
      port: "Puerto",
      port_plural: "Puertos",
      probability: {
        25: "25% Difícil de vulnerar",
        50: "50% Posible de vulnerar",
        75: "75% Fácil de vulnerar",
        100: "100% Vulnerado Anteriormente",
        title: "Probabilidad",
      },
      recommendation: "Recomendación",
      remediation_modal: {
        justification: "¿Cuál fue la solución aplicada?",
        title: "Hallazgo remediado",
      },
      reportLevel: {
        detailed: "Detallado",
        general: "General",
        title: "Nivel de reporte",
      },
      request_verify: "Solicitar verificación",
      requirements: "Requisitos",
      risk: "Riesgo",
      risk_level: "Nivel del riesgo",
      scenario: {
        anon_inter: "Anónimo desde Internet",
        anon_intra: "Anónimo desde Intranet",
        auth_extra: "Usuario de Extranet autorizado",
        auth_inter: "Usuario de Internet autorizado",
        auth_intra: "Usuario de Intranet autorizado",
        title: "Escenario",
        unauth_extra: "Usuario de Extranet no autorizado",
        unauth_inter: "Usuario de Internet no autorizado",
        unauth_intra: "Usuario de Intranet no autorizado",
      },
      severity: "Severidad",
      tab_title: "Descripción",
      threat: "Amenaza",
      title: "Título",
      treatment: {
        accepted: "Asumido",
        in_progress: "En progreso",
        new: "Nuevo",
        title: "Tratamiento",
      },
      treatment_just: "Justificación del tratamiento",
      treatment_mgr: "Responsable del tratamiento",
      type: {
        hygiene: "Higiene",
        security: "Seguridad",
        title: "Tipo de hallazgo",
      },
      update: "Actualizar",
      update_vulnerabilities: "Actualizar Vulnerabilidades",
      vulnDeleted: "La vulnerabilidad fue borrada de este hallazgo",
      weakness: "Debilidad",
      where: "Dónde",
    },
    tab_evidence: {
      animation_exploit: "Animación de explotación",
      detail: "Detalle",
      editable: "Editar",
      evidence_exploit: "Evidencia de explotación",
      tab_title: "Evidencia",
      update: "Actualizar",
    },
    tab_exploit : {
      tab_title: "Exploit",
    },
    tab_indicators: {
      tags: {
        modal_title: "Agregar información de los tags",
      },
    },
    tab_observations: {
      tab_title: "Observaciones",
    },
    tab_records: {
      tab_title: "Registros",
    },
    tab_resources: {
      add_repository: "Agregar",
      branch: "Rama",
      description: "Descripción",
      download: "Descargar",
      environment: "Ambiente",
      environments_title: "Ambientes",
      files_title: "Archivos",
      invalid_chars: "El nombre del archivo contiene caracteres inválidos.",
      modal_env_title: "Agregar información de los ambientes",
      modal_file_title: "Agregar archivo",
      modal_repo_title: "Agregar información de los repositorios",
      no_selection: "Debe seleccionar un ítem de la tabla.",
      remove_repository: "Remover",
      repeated_item: "Uno o varios ítems a añadir ya existen.",
      repositories_title: "Repositorios",
      repository: "URL Repositorio",
      success: "Ítem agregado exitosamente.",
      success_remove: "Ítem eliminado exitosamente.",
    },
    tab_severity: {
      authentication: "Autenticación",
      authentication_options: {
        multiple_auth: "Múltiple: Múltiples puntos de autenticación",
        no_auth: "Ninguna: No se requiere autenticación",
        single_auth: "Única: Único punto de autenticación",
      },
      availability: "Impacto Disponibilidad",
      availability_options: {
        complete: "Completo: Hay una caída total del objetivo",
        none: "Ninguno: No se presenta ningún impacto",
        partial: "Parcial: Se presenta intermitencia en el acceso al objetivo",
      },
      complexity: "Complejidad Acceso",
      complexity_options: {
        high_complex: "Alto: Se requieren condiciones especiales como acceso administrativo",
        low_complex: "Bajo: No se requiere ninguna condición especial",
        medium_complex: "Medio: Se requieren algunas condiciones como acceso al sistema",
      },
      confidence: "Nivel Confianza",
      confidence_options: {
        confirmed: "Confirmado: La vulnerabilidad es reconocida por el fabricante",
        not_confirm: "No confirmado: Existen pocas fuentes que reconocen la vulnerabilidad",
        not_corrob: "No corroborado: La vulnerabilidad es reconocida por fuentes no oficiales",
      },
      confidentiality: "Impacto Confidencialidad",
      confidentiality_options: {
        complete: "Completo: Se controla toda la información relacionada con el objetivo",
        none: "Ninguno: No se presenta ningún impacto",
        partial: "Parcial: Se obtiene acceso a la información pero no control sobre ella",
      },
      cvss_version: "Versión CVSS",
      editable: "Editar",
      exploitability: "Explotabilidad",
      exploitability_options: {
        conceptual: "Conceptual: Existen pruebas de laboratorio",
        functional: "Funcional: Existe exploit",
        high: "Alta: No se requiere exploit o se puede automatizar",
        improbable: "Improbable: No existe un exploit",
      },
      integrity: "Impacto Integridad",
      integrity_options: {
        complete: "Completo: Es posible modificar toda la información del objetivo",
        none: "Ninguno: No se presenta ningún impacto",
        partial: "Parcial: Es posible modificar cierta información del objetivo",
      },
      resolution: "Nivel Resolución",
      resolution_options: {
        non_existent: "Inexistente: No existe solución",
        official: "Oficial: Existe un parche disponible por el fabricante",
        palliative: "Paliativa: Existe un parche que no fue publicado por el fabricante",
        temporal: "Temporal: Existen soluciones temporales",
      },
      tab_title: "Severidad",
      update: "Actualizar",
      vector: "Vector de Acceso",
      vector_options: {
        adjacent: "Red adyacente: Explotable desde el mismo segmento de red",
        local: "Local: Explotable con acceso local al objetivo",
        network: "Red: Explotable desde Internet",
      },
    },
    tab_tracking: {
      closed: "Cerradas",
      cycle: "Ciclo",
      effectiveness: "Efectividad",
      founded: "Encontrado",
      open: "Abiertas",
      tab_title: "Seguimiento",
    },
    tab_users: {
      add_button: "Agregar",
      admin: "Admin",
      analyst: "Analista",
      customer: "Usuario",
      customer_admin: "Manager",
      days_ago: "{{count}} día atrás",
      days_ago_plural: "{{count}} días atrás",
      edit: "Editar",
      edit_user_title: "Editar información del usuario",
      email: "alguien@dominio.com",
      hours_ago: "{{count}} hora atrás",
      hours_ago_plural: "{{count}} horas atrás",
      minutes_ago: "{{count}} minuto atrás",
      minutes_ago_plural: "{{count}} minutos atrás",
      months_ago: "{{count}} mes atrás",
      months_ago_plural: "{{count}} meses atrás",
      no_selection: "Debe seleccionar un correo de la tabla.",
      phone_number: "Número Telefónico",
      remove_user: "Remover",
      responsibility_placeholder: "Product Owner, Gerente del " +
                                    "proyecto, Tester, ...",
      role: "Rol",
      success: " fue agregado a este proyecto exitosamente.",
      success_admin: "Información de usuario actualizada.",
      success_delete: " fue removido del proyecto.",
      textbox: "Ingresa el correo de la persona que deseas agregar, este " +
                  "debe ser un correo de Office 365 o Google.",
      title: "Agregar usuario a este proyecto",
      title_success: "Felicitaciones",
      user_organization: "Organización",
      user_responsibility: "Responsabilidad",
    },
    users_table: {
      firstlogin: "Primer ingreso",
      lastlogin: "Último ingreso",
      phoneNumber: "Número Telefónico",
      userOrganization: "Organización",
      userResponsibility: "Responsabilidad",
      userRole: "Rol",
      usermail: "Email",
    },
  },
  validations: {
    between: "Este valor debe estar entre {{min}} y {{max}}",
    email: "El formato de email no es válido",
    minLength: "Este campo requiere por lo menos {{count}} caracteres",
    numeric: "Este campo sólo puede contener números",
    required: "Este campo es obligatorio",
    tags: "Este campo sólo puede contener caracteres alfanuméricos y guiones medios",
  },
};

export = esTranslations;

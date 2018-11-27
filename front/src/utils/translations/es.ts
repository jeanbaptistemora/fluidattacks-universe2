const esTranslations: Map<string, string> = {
  confirmmodal: {
    cancel: "Cancelar",
    proceed: "Proceder",
  },
  legalNotice: {
    acceptBtn: {
      text: "Aceptar y continuar",
      tooltip: "Haz click si entiendes y aceptas los términos anteriores",
    },
    description: "Integrates, Copyright (c) 2018 FLUID. Esta plataforma \
    contiene información de propiedad de Fluidsignal Group. Dicha información \
    puede ser usada por el cliente sólo con el propósito de documentación sin \
    poder divulgar su contenido a terceras partes ya que contiene ideas, \
    conceptos, precios y/o estructuras de propiedad de Fluidsignal Group S.A. \
    La clasificación 'propietaria' significa que esta información es solo para \
    uso de las personas a quienes está dirigida. En caso de requerirse copias \
    totales o parciales se debe contar con la autorización expresa y escrita de \
    Fluidsignal Group S.A. Las normas que fundamentan la clasificación de la \
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
    file_updated: "Archivo Actualizado ;)",
    no_file_selected: "No se ha seleccionado ningún archivo",
    no_file_update: "Falló al actualizar el archivo",
    title_success: "Felicitaciones",
  },
  search_findings: {
    environment_table: {
      environment: "Ambiente",
    },
    repositories_table: {
      branch: "Rama",
      repository: "Repositorio",
    },
    tab_description: {
      action: "Acción",
      errorFileVuln: "El archivo de vulnerabilidades tiene errores",
      field: "Campo",
      inputs: "Entradas",
      line: "Línea",
      line_plural: "Líneas",
      path: "Ruta",
      port: "Puerto",
      port_plural: "Puertos",
      vulnDeleted: "La vulnerabilidad fue borrada de este hallazgo",
    },
    tab_evidence: {
      editable: "Editar",
      update: "Actualizar",
    },
    tab_resources: {
      add_repository: "Agregar",
      branch: "Rama",
      environment: "Ambiente",
      environments_title: "Ambientes",
      modal_env_title: "Agregar información de los ambientes",
      modal_repo_title: "Agregar información de los repositorios",
      no_selection: "Debe seleccionar un ítem de la tabla.",
      remove_repository: "Remover",
      repeated_item: "Uno o varios ítems a añadir ya existen.",
      repositories_title: "Repositorios",
      repository: "Repositorio",
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
};

export = esTranslations;

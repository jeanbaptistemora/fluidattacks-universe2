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
    no_file_selected: "No se ha seleccionado ningún archivo",
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
    tab_resources: {
      add_repository: "Agregar",
      branch: "Rama",
      environment: "Ambiente",
      environments_title: "Ambientes",
      modal_env_title: "Agregar información de los ambientes",
      modal_repo_title: "Agregar información de los repositorios",
      no_selection: "Debe seleccionar un item de la tabla.",
      remove_repository: "Remover",
      repeated_item: "Uno o varios items a añadir ya existen.",
      repositories_title: "Repositorios",
      repository: "Repositorio",
      success: "Item agregado exitosamente.",
      success_remove: "Item eliminado exitosamente.",
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

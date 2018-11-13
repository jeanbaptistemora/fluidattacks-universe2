interface ITranslationMap { [key: string]: string | ITranslationMap; }

const esTranslations: ITranslationMap = {
  confirmmodal: {
    cancel: "Cancelar",
    proceed: "Proceder",
  },
  proj_alerts: {
    error_textsad: "Hay un error :(",
  },
  search_findings: {
    tab_users: {
      admin: "Admin",
      analyst: "Analista",
      customer: "Usuario",
      customer_admin: "Manager",
      edit_user_title: "Editar información del usuario",
      email: "alguien@dominio.com",
      phone_number: "Número Telefónico",
      responsibility_placeholder: "Product Owner, Gerente del " +
                                    "proyecto, Tester, ...",
      role: "Rol",
      textbox: "Ingresa el correo de la persona que deseas agregar, este " +
                  "debe ser un correo de Office 365 o Google.",
      title: "Agregar usuario a este proyecto",
      user_organization: "Organización",
      user_responsibility: "Responsabilidad",
    },
  },
};

export = esTranslations;

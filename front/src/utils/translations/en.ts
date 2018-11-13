interface ITranslationMap { [key: string]: string | ITranslationMap; }

const enTranslations: ITranslationMap = {
  confirmmodal: {
    cancel: "Cancel",
    proceed: "Proceed",
  },
  proj_alerts: {
    error_textsad: "There is an error :(",
  },
  search_findings: {
    tab_users: {
      admin: "Admin",
      analyst: "Analyst",
      customer: "User",
      customer_admin: "Manager",
      edit_user_title: "Edit user information",
      email: "someone@domain.com",
      phone_number: "Phone Number",
      responsibility_placeholder: "Product Owner, Project Manager, " +
                                     "Tester, ...",
      role: "Role",
      textbox: "Enter the email of the person you wish to add, it must be " +
                   "an Office 365 or Google email",
      title: "Add user to this project",
      user_organization: "Organization",
      user_responsibility: "Responsibility",
    },
  },
};

export = enTranslations;

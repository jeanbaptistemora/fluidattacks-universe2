const enTranslations: Map<string, string> = {
  confirmmodal: {
    cancel: "Cancel",
    proceed: "Proceed",
  },
  legalNotice: {
    acceptBtn: {
      text: "Accept and continue",
      tooltip: "Click if you understand and accept the terms above",
    },
    description: "Integrates, Copyright (c) 2018 FLUID. This platform contains \
    information proprietary of Fluidsignal Group. The client is only allowed \
    to use such information for documentation purposes and without disclosing \
    its content to third parties because it may contain ideas, concepts, prices \
    and/or structures propriety of Fluidsignal Group S.A. Its 'proprietary' \
    classification means that this information will only be used by those who \
    it was meant for. In case of requiring total or partial reproductions it \
    must be done with express and written authorization of Fluidsignal Group \
    S.A. The rules that fundament the classification of information are \
    articles 72, Cartagena's agreement 344 of 1.993, article 238 of penal code \
    and articles 16 and its following ones from 256 law of 1.996.",
    rememberCbo: {
      text: "Remember my decision",
      tooltip: "Mark the checkbox if you want this decision to be permanent",
    },
    title: "Legal notice",
  },
  proj_alerts: {
    error_textsad: "There is an error :(",
    title_success: "Congratulations",
  },
  search_findings: {
    environment_table: {
      environment: "Environment",
    },
    repositories_table: {
      branch: "Branch",
      repository: "Repository",
    },
    tab_description: {
      action: "Action",
      errorFileVuln: "Vulnerabilities file has errors",
      field: "Field",
      inputs: "Inputs",
      line: "Line",
      line_plural: "Lines",
      path: "Path",
      port: "Port",
      port_plural: "Ports",
      vulnDeleted: "Vulnerability was deleted of this finding",
    },
    tab_resources: {
      add_repository: "Add",
      branch: "Branch",
      environment: "Environment",
      environments_title: "Environments",
      modal_env_title: "Add environment information",
      modal_repo_title: "Add repository information",
      no_selection: "You must select an item from the table.",
      remove_repository: "Remove",
      repeated_item: "One or more items to add already exist.",
      repositories_title: "Repositories",
      repository: "Repository",
      success: "Item added successfully.",
      success_remove: "Item removed successfully.",
    },
    tab_users: {
      add_button: "Add",
      admin: "Admin",
      analyst: "Analyst",
      customer: "User",
      customer_admin: "Manager",
      days_ago: "{{count}} day ago",
      days_ago_plural: "{{count}} days ago",
      edit: "Edit",
      edit_user_title: "Edit user information",
      email: "someone@domain.com",
      hours_ago: "{{count}} hour ago",
      hours_ago_plural: "{{count}} hours ago",
      minutes_ago: "{{count}} minute ago",
      minutes_ago_plural: "{{count}} minutes ago",
      months_ago: "{{count}} month ago",
      months_ago_plural: "{{count}} months ago",
      no_selection: "You must select an email from the table.",
      phone_number: "Phone Number",
      remove_user: "Remove",
      responsibility_placeholder: "Product Owner, Project Manager, " +
                                     "Tester, ...",
      role: "Role",
      success: " now has access to this project.",
      success_admin: "User information updated.",
      success_delete: " was removed from this project.",
      textbox: "Enter the email of the person you wish to add, it must be " +
                   "an Office 365 or Google email",
      title: "Add user to this project",
      title_success: "Congratulations",
      user_organization: "Organization",
      user_responsibility: "Responsibility",
    },
    users_table: {
      firstlogin: "First login",
      lastlogin: "Last login",
      phoneNumber: "Phone Number",
      userOrganization: "Organization",
      userResponsibility: "Responsibility",
      userRole: "Role",
      usermail: "User email",
    },
  },
};

export = enTranslations;

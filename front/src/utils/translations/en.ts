const enTranslations: dict = {
  confirmmodal: {
    cancel: "Cancel",
    message: "Are you sure?",
    proceed: "Proceed",
    title_cvssv2: "Update CVSSv2",
    title_generic: "Confirm action",
  },
  forms: {
    closing: "Closure",
    events: "Events",
    findings: "Findings",
    progress: "Progress",
  },
  home: {
    title: "My Projects",
  },
  legalNotice: {
    acceptBtn: {
      text: "Accept and continue",
      tooltip: "Click if you understand and accept the terms above",
    },
    description: "Integrates, Copyright (c) 2019 Fluid Attacks. This platform contains \
    information proprietary of Fluid Attacks. The client is only allowed \
    to use such information for documentation purposes and without disclosing \
    its content to third parties because it may contain ideas, concepts, prices \
    and/or structures propriety of Fluid Attacks. Its 'proprietary' \
    classification means that this information will only be used by those who \
    it was meant for. In case of requiring total or partial reproductions it \
    must be done with express and written authorization of Fluid Attacks. \
    The rules that fundament the classification of information are \
    articles 72, Cartagena's agreement 344 of 1.993, article 238 of penal code \
    and articles 16 and its following ones from 256 law of 1.996.",
    rememberCbo: {
      text: "Remember my decision",
      tooltip: "Mark the checkbox if you want this decision to be permanent",
    },
    title: "Legal notice",
  },
  logout: "Log out",
  navbar: {
    breadcrumbRoot: "My Projects",
    searchPlaceholder: "Project Name",
  },
  proj_alerts: {
    access_denied: "Access denied or project not found",
    error_textsad: "There is an error :(",
    file_size: "The file size must be less than 10MB",
    file_size_png: "The image size must be less than 2MB",
    file_size_py: "The file size must be less than 1MB",
    file_type_csv: "The file must be .csv type",
    file_type_gif: "The image must be .gif type",
    file_type_png: "The image must be .png type",
    file_type_py: "The file must be .py type",
    file_type_wrong: "The file has an unknown or non-allowed format",
    file_type_yaml: "The file must be .yaml or .yml type",
    file_updated: "File Updated ;)",
    invalid_schema: "Uploaded file does not match with the schema",
    invalid_specific: "Invalid field/line/port",
    invalid_treatment_mgr: "Please select a treatment manager",
    no_file_selected: "No file selected",
    no_file_update: "Failed to update the file",
    port_value: "Port value should be between 0 and 65535",
    range_error: "Range limits are wrong",
    title_success: "Congratulations",
    updated: "Updated",
    updated_title: "Correct!",
    verified_success: "This finding was marked as verified.",
  },
  project: {
    findings: {
      exploitable: {
        no: "No",
        yes: "Yes",
      },
      exportCsv: "Export to CSV",
      help_label: "Click on a finding to see more details",
      report: {
        btn: "Reports",
        modal_close: "Close",
        modal_title: "Reports",
        tech_description: "Technical report is protected by password."
        + "The password is the date of report's PDF generation and your username.",
        tech_example: "Example: someone@fluidattacks.com generates the technical report on 15/03/2019 therefore, "
        + "the password is 15032019someone",
        tech_title: "Technical Reports",
      },
    },
    tabs: {
      comments: "Comments",
      drafts: "Drafts",
      events: "Events",
      findings: "Findings",
      indicators: "Indicators",
      resources: "Resources",
      users: "Users",
    },
  },
  registration: {
    continue_btn: "Continue as",
    greeting: "Hello",
    logged_in_message: "Please log out before trying to access with another account.",
    logged_in_title: "You are already logged in",
    unauthorized: "You do not have authorization for login yet. Please contact Fluid Attacks's staff or your project " +
      "administrator to get access.",
  },
  search_findings: {
    alert: {
      attention: "Attention",
    },
    critical_severity: "Critical",
    delete: {
      justif: {
        duplicated: "It is duplicated",
        evidence_change: "Change of evidence",
        finding_change: "Finding has changed",
        label: "Justification",
        not_vuln: "It is not a Vulnerability",
      },
      title: "Delete Finding",
    },
    draft_approved: "This finding has been approved",
    environment_table: {
      environment: "Environment",
    },
    files_table: {
      description: "Description",
      file: "File",
      upload_date: "Upload Date",
    },
    finding_deleted: "Finding {{findingId}} has been deleted",
    high_severity: "High",
    low_severity: "Tolerable",
    medium_severity: "Moderate",
    openVulnsLabel: "Open vulnerabilities",
    reject: "Reject Draft",
    reportDateLabel: "Report date",
    repositories_table: {
      branch: "Branch",
      protocol: "Protocol",
      repository: "Repository URL",
    },
    severityLabel: "Severity",
    status: {
      closed: "Closed",
      open: "Open",
    },
    statusLabel: "Status",
    tab_comments: {
      tab_title: "Comments",
    },
    tab_description: {
      action: "Action",
      actor: {
        any_customer: "Any customer of the organization",
        any_employee: "Any employee of the organization",
        any_internet: "Anyone on Internet",
        any_station: "Anyone with access to the station",
        one_employee: "Only one employee",
        some_customer: "Only some customers of the organization",
        some_employee: "Only some employees",
        title: "Actor",
      },
      affected_systems: "Affected systems",
      ambit: {
        applications: "Applications",
        databases: "Databases",
        infra: "Infrastructure",
        sourcecode: "Source code",
        title: "Ambit",
      },
      attack_vectors: "Attack vectors",
      bts: "External BTS",
      category: {
        define_auth_model: "Define the authorization model considering the principle of least privilege",
        event: "Eventuality",
        expose_tech_info: "Avoid exposing technical information of the application, servers and platforms",
        http_req_integrity: "Validate transactions integrity in HTTP requests",
        log_events: "Log events for traceability and auditory",
        maintainability: "Maintainability",
        performance: "Performance",
        secure_protocols: "Use secure communication protocols",
        sensible_data_code: "Exclude sensible data from source code and event logging",
        strengthen_auth_session: "Strengthen authentication and session management controls",
        strengthen_file_processing: "Strengthen file processing controls",
        strengthen_password_keys: "Strengthen protection of stored data related with passwords and cryptographic keys",
        title: "Category",
        update_sec_baselines: "Update and configure the security baselines of components",
        validate_input: "Implement controls for input validation",
      },
      compromised_attrs: "Compromised attributes",
      compromised_records: "Compromised records",
      customer_project_code: "Customer's project code",
      customer_project_name: "Customer's project name",
      description: "Description",
      download_vulnerabilities: "Download Vulnerabilities",
      editable: "Edit",
      errorFileVuln: "Vulnerabilities file has errors",
      field: "Field",
      inputs: "Inputs",
      kb: "Solution URL",
      line: "Line",
      line_plural: "Lines",
      mark_verified: "Verify",
      path: "Path",
      port: "Port",
      port_plural: "Ports",
      probability: {
        25: "25% Hard to exploit",
        50: "50% Possible to exploit",
        75: "75% Easy to exploit",
        100: "100% Exploited before",
        title: "Probability",
      },
      recommendation: "Recommendation",
      remediation_modal: {
        justification: "Which was the applied solution?",
        title: "Finding remediated",
      },
      reportLevel: {
        detailed: "Detailed",
        general: "General",
        title: "Report level",
      },
      request_verify: "Request verification",
      requirements: "Requirements",
      risk: "Risk",
      risk_level: "Risk level",
      scenario: {
        anon_inter: "Anonymous from Internet",
        anon_intra: "Anonymous from Intranet",
        auth_extra: "Authorized Extranet user",
        auth_inter: "Authorized Internet user",
        auth_intra: "Authorized Intranet user",
        title: "Scenario",
        unauth_extra: "Unauthorized Extranet user",
        unauth_inter: "Unauthorized Internet user",
        unauth_intra: "Unauthorized Intranet user",
      },
      severity: "Severity",
      tab_title: "Description",
      threat: "Threat",
      title: "Title",
      treatment: {
        accepted: "Accepted",
        in_progress: "In progress",
        new: "New",
        title: "Treatment",
      },
      treatment_just: "Treatment justification",
      treatment_mgr: "Treatment manager",
      type: {
        hygiene: "Hygiene",
        security: "Security",
        title: "Finding type",
      },
      update: "Update",
      update_vulnerabilities: "Update Vulnerabilities",
      vulnDeleted: "Vulnerability was deleted of this finding",
      weakness: "Weakness",
      where: "Where",
    },
    tab_events: {
      affectation: "Affectation",
      affected_components: "Affected components",
      analyst: "Analyst",
      client: "Client",
      client_project: "Client's Project",
      date: "Date",
      description: "Description",
      edit: "Edit",
      event_in: "Event present in",
      evidence: "Evidence",
      fluid_project: "Fluid Attacks' Project",
      id: "ID",
      resume: "Resume",
      status: "Status",
      status_values: {
        solve: "Solved",
        unsolve: "Unsolved",
      },
      table_advice: "Click on an event to see more details",
      type: "Type",
      type_values: {
        approv_change: "Client approves the change of ToE",
        auth_attack: "Authorization for special attack",
        cancel_proj: "Client cancels the project/milestone",
        det_attack: "Client detects an attack",
        explic_suspend: "Client explicitly suspends project",
        high_approval: "High availability approval",
        inacc_ambient: "Inaccessible ambient",
        incor_supplies: "Incorrect or missing supplies",
        other: "Other",
        toe_differs: "ToE differs from what was approved",
        uns_ambient: "Unstable ambient",
      },
    },
    tab_evidence: {
      animation_exploit: "Exploitation animation",
      detail: "Detail",
      editable: "Edit",
      evidence_exploit: "Exploitation evidence",
      tab_title: "Evidence",
      update: "Update",
    },
    tab_exploit: {
      tab_title: "Exploit",
    },
    tab_indicators: {
      authors: "Current month authors",
      closed: "Closed",
      closed_percentage: "Closed vulnerabilities",
      commits: "Current month commits",
      days: "days",
      git_title: "Git Indicators",
      last_closing_vuln: "Days since last closed vulnerability",
      max_open_severity: "Max open severity",
      max_severity: "Max severity found",
      mean_remediate: "Mean time to remediate",
      open: "Open",
      pending_closing_check: "Pending closing verification",
      project_title: "Project Indicators",
      repositories: "Analyzed Repositories",
      status_graph: "Status",
      tags: {
        modal_title: "Add tags information",
      },
      total_findings: "Total Findings",
      total_vulnerabilitites: "Total Vulnerabilities",
      treatment_accepted: "Accepted",
      treatment_graph: "Treatment",
      treatment_in_progress: "In progress",
      treatment_no_defined: "No defined",
      undefined_treatment: "Open vulnerabilities with no defined treatment",
    },
    tab_observations: {
      tab_title: "Observations",
    },
    tab_records: {
      tab_title: "Records",
    },
    tab_resources: {
      add_repository: "Add",
      base_url_placeholder: "gitlab.com/fluidattacks/integrates.git",
      branch: "Branch",
      branch_placeholder: "master",
      description: "Description",
      download: "Download",
      environment: "Environment",
      environments_title: "Environments",
      files_title: "Files",
      https: "HTTPS",
      invalid_chars: "File name has invalid characters.",
      modal_env_title: "Add environment information",
      modal_file_title: "Add file",
      modal_options_content: "What do you want to do with file ",
      modal_options_title: "File options",
      modal_repo_title: "Add repository information",
      no_file_upload: "Failed to upload the file",
      no_selection: "You must select an item from the table.",
      protocol: "Protocol",
      remove_repository: "Remove",
      repeated_item: "One or more items to add already exist.",
      repositories_title: "Repositories",
      repository: "Repository URL",
      ssh: "SSH",
      success: "Item added successfully.",
      success_remove: "Item removed successfully.",
      tags_title: "Tags",
      total_envs: "Total environments: ",
      total_files: "Total files: ",
      total_repos: "Total repositories: ",
      total_tags: "Total tags: ",
      uploading_progress: "Uploading file...",
    },
    tab_severity: {
      attack_complexity: "Attack Complexity",
      attack_complexity_options: {
        high: "High",
        low: "Low",
      },
      attack_vector: "Attack Vector",
      attack_vector_options: {
        adjacent: "Adjacent network",
        local: "Local",
        network: "Network",
        physical: "Physical",
      },
      authentication: "Authentication",
      authentication_options: {
        multiple_auth: "Multiple: Multiple authentication points",
        no_auth: "None: Authentication is not required",
        single_auth: "Single: Single authentication point",
      },
      availability: "Availability Impact",
      availability_impact: "Availability Impact",
      availability_impact_options: {
        high: "High",
        low: "Low",
        none: "None",
      },
      availability_options: {
        complete: "Complete: There is a total target down",
        none: "None: There is no impact",
        partial: "Partial: There is intermittency in the access to the target",
      },
      availability_requirement: "Availability Requirement",
      availability_requirement_options: {
        high: "High",
        low: "Low",
        medium: "Medium",
      },
      complexity: "Access Complexity",
      complexity_options: {
        high_complex: "High: Special conditions are required like administrative access",
        low_complex: "Low: No special conditions are required",
        medium_complex: "Medium: Some conditions are required like system access",
      },
      confidence: "Confidence Level",
      confidence_options: {
        confirmed: "Confirmed: The vulnerability is recognized by the manufacturer",
        not_confirm: "Not confirmed: There are few sources that recognize vulnerability",
        not_corrob: "Not corroborared: Vulnerability is recognized by unofficial sources",
      },
      confidentiality: "Confidentiality Impact",
      confidentiality_impact: "Confidentiality Impact",
      confidentiality_impact_options: {
        high: "High",
        low: "Low",
        none: "None",
      },
      confidentiality_options: {
        complete: "Complete: Total control over information related with the target",
        none: "None: There is no impact",
        partial: "Partial: Access to information but no control over it",
      },
      confidentiality_requirement: "Confidentiality Requirement",
      confidentiality_requirement_options: {
        high: "High",
        low: "Low",
        medium: "Medium",
      },
      cvss_version: "CVSS Version",
      editable: "Edit",
      exploitability: "Exploitability",
      exploitability_options: {
        conceptual: "Conceptual: There are laboratory tests",
        functional: "Functional: There is an exploit",
        high: "High: Exploit is not required or it can be automated",
        improbable: "Improbable: There is no exploit",
        proof_of_concept: "Proof of Concept",
        unproven: "Unproven",
      },
      integrity: "Integrity Impact",
      integrity_impact: "Integrity Impact",
      integrity_impact_options: {
        high: "High",
        low: "Low",
        none: "None",
      },
      integrity_options: {
        complete: "Complete: Posibility of modify all target information",
        none: "None: There is no impact",
        partial: "Partial: Posibility of modify some target information",
      },
      integrity_requirement: "Integrity Requirement",
      integrity_requirement_options: {
        high: "High",
        low: "Low",
        medium: "Medium",
      },
      modified_attack_complexity: "Modified Attack Complexity",
      modified_attack_vector: "Modified Attack Vector",
      modified_availability_impact: "Modified Availability Impact",
      modified_confidentiality_impact: "Modified Confidentiality Impact",
      modified_integrity_impact: "Modified Integrity Impact",
      modified_privileges_required: "Modified Privileges Required",
      modified_severity_scope: "Modified Scope",
      modified_user_interaction: "Modified User Interaction",
      privileges_required: "Privileges Required",
      privileges_required_options: {
        high: "High",
        low: "Low",
        none: "None",
      },
      remediation_level: "Remediation Level",
      remediation_level_options: {
        official_fix: "Official Fix",
        temporary_fix: "Temporary Fix",
        unavailable: "Unavailable",
        workaround: "Workaround",
      },
      report_confidence: "Report Confidence",
      report_confidence_options: {
        confirmed: "Confirmed",
        reasonable: "Reasonable",
        unknown: "Unknown",
      },
      resolution: "Resolution Level",
      resolution_options: {
        non_existent: "Non-existent: There is no solution",
        official: "Official: There is an manufacturer available patch",
        palliative: "Palliative: There is a patch that was not published by the manufacturer",
        temporal: "Temporal: There are temporary solutions",
      },
      severity_scope: "Scope",
      severity_scope_options: {
        changed: "Changed",
        unchanged: "Unchanged",
      },
      tab_title: "Severity",
      update: "Update",
      user_interaction: "User Interaction",
      user_interaction_options: {
        none: "None",
        required: "Required",
      },
      vector: "Access Vector",
      vector_options: {
        adjacent: "Adjacent network: Exploitable from same network segment",
        local: "Local: Exploitable with local access to the target",
        network: "Network: Exploitable from Internet",
      },
    },
    tab_tracking: {
      closed: "Closed",
      cycle: "Cycle",
      effectiveness: "Effectiveness",
      founded: "Found",
      open: "Open",
      tab_title: "Tracking",
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
  sidebar: {
    forms: "Formstack",
  },
  validations: {
    between: "This value must be between {{min}} and {{max}}",
    email: "The email format is not valid",
    file_size: "The file size must be less than {{count}}MB",
    minLength: "This field requires at least {{count}} characters",
    numeric: "This field can only contain numbers",
    required: "This field is required",
    tags: "This field can only contain alphanumeric characters and dashes",
  },
};

export = enTranslations;

// tslint:disable:max-file-line-count

const enTranslations: Dictionary = {
  analytics: {
    disjointForceDirectedGraph: {
      whereToFindings: {
        footer: {
          grey: "Each grey dot represents a resource (IP, URL, or repository).",
          redAndGreen: "Red and green dots represent the open and closed findings for that system, respectively.",
          size: "Size and darkness are proportional to the security impact on that system.",
        },
        title: "Systems Risk",
      },
    },
    gauge: {
      forcesBuildsRisk: {
        footer: {
          intro: "Risk is proportional to the number of vulnerable changes introduced into your system:",
          preventedVulnerableBuilds: "Forces in strict mode stops those security issues from "
            + "being delivered to your end users.",
          vulnerableBuilds: "A build is considered vulnerable if it contains security issues.",
        },
        title: "Builds risk",
      },
      forcesSecurityCommitment: {
        footer: {
          acceptedRisk: "However, accepted vulnerabilities on Integrates are ignored by the strict mode, "
            + "and Forces will (by decision of your team) allow them to be built or deployed.",
          conclusion: "The maximum benefit is reached when the accepted risk is low, and the strict mode high.",
          intro: "Forces objective is to help your team overcome security vulnerabilities. "
            + "For this to work, we put two things in your hands:",
          strictMode: "The strict mode (which is enabled by default) helps you stop builds or deployments "
            + "if there are open vulnerabilities, and thus protects your system from vulnerable code introduction.",
        },
        title: "Your commitment towards security",
      },
      severity: {
        footer: "Security vulnerabilities are ranked based on C.V.S.S. v3.1. "
          + "The higher the score, "
          + "the more damage an attack can make to your system, "
          + "and the easier it is to carry it on",
        title: "Severity",
      },
    },
    headers: {
      forces: {
        title: "Forces",
      },
    },
    pieChart: {
      resources: {
        footer: {
          environments: "Environment: A URL or IP pointing to an instance of your system.",
          final: "The maximum benefit is reached when every environment has"
            + " its full source-code available for us to test it.",
          intro: "Resources can be of two types: Repository and Environment.",
          repositories: "Repository: The associated source-code of the environment "
            + "and (ideally) its infrastructure.",
        },
        title: "Active resources distribution",
      },
      status: {
        footer: {
          intro: "Ratio of open to closed vulnerabilities, ignoring treatments.",
        },
        title: "Vulnerabilities status",
      },
      treatment: {
        footer: {
          accepted: "Temporarily accepted: A manager decided to temporarily coexist with the risk.",
          eternally: "Eternally accepted: A vulnerability that will never be remediated.",
          inProgress: "In progress: The system is currently being hardened by your developers.",
          intro: "At Integrates you can plan and manage the remediation of security findings:",
          notDefined: "Not defined: New vulnerabilities goes here until one of your managers generate an action plan.",
        },
        title: "Vulnerabilities treatment",
      },
    },
    stackedBarChart: {
      riskOverTime: {
        footer: {
          accepted: "Open vulnerabilities with accepted treatment are exactly as the open ones"
            + ", except you decided to coexist with that risk.",
          closed: "Closed vulnerabilities may be seen as security breaches your system no longer have.",
          intro: "At Integrates you can track the evolution of your systems from a security point of view:",
          opened: "Open vulnerabilities represent a risk currently impacting your end-users and systems.",
        },
        title: "Vulnerabilities over time",
      },
    },
    textBox: {
      daysSinceLastRemediation: {
        footer: "Days since a finding was effectively closed.",
        title: "Days since last remediation",
      },
      findingsBeingReattacked: {
        footer: "Once your team has solved a vulnerability you can request a re-attack. "
          + "In the re-attack process a hacker will replay the attack vector and confirm that "
          + "the proposed solution actually shields your system. "
          + "In case it does not, your team will be notified and the finding kept open.",
        title: "Findings being re-attacked",
      },
      forcesAutomatizedVulns: {
        footer: "Forces performs security testing of your source-code, deployed environment and infrastructure. "
          + "Single units of security problems found are displayed here.",
        title: "Automatized Vulnerabilities",
      },
      forcesRepositoriesAndBranches: {
        footer: "You can run Forces in any of your repositories at any of its versions (commits or branches).",
        title: "Repositories and branches",
      },
      forcesStatus: {
        footer: {
          breaks: "In case Forces finds one vulnerability to be open, "
            + "we can (optionally) mark the build as failed so you never introduce known vulnerabilities "
            + "into the production environment.",
          intro: "By enabling Forces you get access to a Docker container built to specifically verify the status "
            + "of security findings found in your system. "
            + "You can embed this container in your Continuous Integration system in order "
            + "to test changes for security vulnerabilities:",
          smart: "Forces is fast and automatic, yet made by the same hackers intelligence "
            + "that already know in deep your system, and thus is able to verify attack vectors that no "
            + "other tool can.",
          stats: "The statistics of more than a hundred different systems show that Forces increases "
            + "the remediation ratio, hence helping you build a safer system, and being more cost-effective "
            + "throughout your Software Security Development Life Cycle.",
        },
        title: "Service status",
      },
      forcesUsage: {
        footer: "Number of times your team used Forces to check for vulnerabilities.",
        title: "Service usage",
      },
      totalFindings: {
        footer: "A finding is a group of vulnerabilities on your system "
          + "related to the same attack vector.",
        title: "Total findings",
      },
      totalVulnerabilities: {
        footer: "Vulnerabilities are the minimum units of risk. "
          + "They are tied to a system, and a specific location within that system.",
        title: "Total vulnerabilities",
      },
    },
  },
  confirmmodal: {
    cancel: "Cancel",
    message: "Are you sure?",
    proceed: "Proceed",
    title_cvssv2: "Update CVSSv2",
    title_generic: "Confirm action",
  },
  dataTableNext: {
    filters: "Filters",
    more: "--More--",
    noDataIndication: "There is no data to display",
    tooltip: "filters of search on the table",
  },
  delete_vulns: {
    not_success: "Vulnerability could not be eliminated",
    reporting_error: "Error while reporting",
    title: "Delete Vulnerability",
  },
  forms: {
    closing: "Closure",
    events: "Events",
    findings: "Findings",
    progress: "Progress",
  },
  group: {
    authors: {
      actor: "Author",
      commit: "Commit",
      groups_contributed: "Groups Contributed",
      repository: "Repository",
      table_advice: "Below you'll find the authors that have contributed "
      + "to your group in the selected month, and one example commit",
    },
    drafts: {
      approve: {
        text: "Approve",
        title: "Approve draft",
        tooltip: "Accept the finding",
      },
      btn: {
        text: "New",
        tooltip: "Create a new finding",
      },
      error_submit: "Please provide {{missingFields}} before submitting",
      new: "New Finding",
      reject: {
        text: "Reject",
        title: "Reject Draft",
        tooltip: "Cancel the request for review the finding",
      },
      submit: {
        text: "Submit",
        tooltip: "Submit the finding for review",
      },
      success_create: "Draft created successfully",
      success_submit: "Draft successfully submitted for review",
      title: "Title",
      title_success: "Success",
    },
    events: {
      alreadyClosed: "This event has already been closed",
      btn: {
        text: "New",
        tooltip: "Create a new event",
      },
      description: {
        solved: {
          affectation: "Affectation (hours)",
          date: "Resolution date",
        },
      },
      evidence: {
        edit: "Edit",
        no_data: "There are no evidences",
      },
      form: {
        accessibility: {
          environment: "Environment",
          repository: "Repository",
          title: "Accessibility",
        },
        action_after: {
          other_other: "Execute another group of a different client",
          other_same: "Execute another group of the same client",
          title: "Action after getting blocked",
          training: "Training",
        },
        action_before: {
          document: "Document group",
          test_other: "Test other part of ToE",
          title: "Action before blocking",
        },
        blocking_hours: "Working hours until getting blocked",
        components: {
          client_station: "Client's test station",
          compile_error: "Compilation error",
          documentation: "Group documentation",
          fluid_station: "FLUID's test station",
          internet_conn: "Internet connectivity",
          local_conn: "Local connectivity (LAN, WiFi)",
          source_code: "Source code",
          test_data: "Test data",
          title: "Affected components",
          toe_alteration: "ToE alteration",
          toe_credentials: "ToE credentials",
          toe_exclussion: "ToE exclussion",
          toe_location: "ToE location (IP, URL)",
          toe_privileges: "ToE privileges",
          toe_unaccessible: "ToE unaccessibility",
          toe_unavailable: "ToE unavailability",
          toe_unstability: "ToE unstability",
          vpn_conn: "VPN connectivity",
        },
        context: {
          client: "Client",
          fluid: "FLUID",
          planning: "Planning",
          telecommuting: "Telecommuting",
          title: "Being at",
        },
        date: "Event date",
        details: "Details",
        evidence: "Evidence image",
        evidence_file: "Evidence file",
        none: "None",
        other: "Other",
        responsible: "Person in charge (client)",
        type: {
          detects_attack: "Client detects the attack",
          high_availability: "High availability approval",
          missing_supplies: "Incorrect or missing supplies",
          special_attack: "Authorization for special attack",
          title: "Type",
          toe_change: "Client approves ToE change",
          toe_differs: "ToE different than agreed upon",
        },
        wrong_file_type: "Evidence files must have .pdf, .zip or .csv extension",
        wrong_image_type: "Evidence images must have .gif, .jpg, or .png extension",
      },
      new: "New Event",
      success_create: "Event created successfully",
      title_success: "Success",
    },
    findings: {
      boolean: {
        False: "No",
        True: "Yes",
      },
      evidence: {
        edit: "Edit",
        no_data: "There are no evidences",
      },
      exploit: {
        no_data: "There is no exploit",
      },
      exportCsv: {
        text: "Export",
        tooltip: "Export to a comma-separated values file",
      },
      help_label: "Click on a finding to see more details",
      records: {
        no_data: "There are no records",
      },
      remediated: {
        False: "-",
        True: "Pending",
      },
      report: {
        btn: {
          text: "Reports",
          tooltip: "Generate a report of findings and send it to your email",
        },
        data: "  DATA",
        modal_close: "Close",
        modal_title: "Reports",
        pdf: "  PDF",
        tech_description:
        "Technical reports are created on-demand and are protected by a <strong>passphrase</strong>. "
        + "The <strong>passphrase</strong> is generated randomly and will be sent to your email along "
        + "with a link to download the requested report.",
        tech_title: "Technical Reports",
        xls: "  XLS",
      },
      tableSet: {
        btn: {
          text: "Columns",
          tooltip: "Choose the fields you want to display",
        },
        modal_title: "Columns Filter",
      },
    },
    forces: {
      compromised_toe: {
        risk_state: "Risk State",
        title: "Compromised Surface",
        type: "Type",
        what: "What",
        where: "Where",
      },
      date: "Date",
      execution_details_modal: {
        close: "Close",
        title: "Execution Details",
      },
      found_vulnerabilities: {
        accepted: "Accepted",
        exploitable: "Exploitable",
        not_exploitable: "Not exploitable",
        title: "Vulnerabilities",
        total: "Total",
      },
      git_repo: "Git Repository",
      identifier: "Identifier",
      kind: {
        dynamic: "Deployed System",
        static: "Source Code",
        title: "Target of Evaluation",
      },
      status: {
        secure: "Secure",
        title: "Status",
        vulnerabilities: "Vulnerabilities",
        vulnerable: "Vulnerable",
      },
      strictness: {
        strict: "Strict",
        title: "Strictness",
        tolerant: "Tolerant",
      },
      table_advice: "Click on an execution to see more details",
    },
    tabs: {
      authors: {
        text: "Authors",
        tooltip: "People that have contributed to your group",
      },
      charts: {
        text: "Charts",
        tooltip: "Group status at a glance",
      },
      comments: {
        text: "Comments",
        tooltip: "Space where all interested parties can share information about the group",
      },
      drafts: {
        text: "Drafts",
        tooltip: "Add new findings and review those yet to be approved",
      },
      events: {
        text: "Events",
        tooltip: "Keep track of all the situations that are affecting the group",
      },
      findings: {
        text: "Findings",
        tooltip: "Keep track of the status of all the approved findings",
      },
      forces: {
        text: "Forces",
        tooltip: "Check the state of the Forces jobs in your CI/CD",
      },
      indicators: {
        text: "Indicators",
        tooltip: "Summary of the group status",
      },
      resources: {
        text: "Settings",
        tooltip: "Configure the resources needed by the security tests and the services to be purchased," +
        " if applicable",
      },
      users: {
        text: "Users",
        tooltip: "Add, edit, and remove users from this group",
      },
    },
  },
  group_alerts: {
    acceptation_approved: "Indefinite acceptation has been approved",
    acceptation_rejected: "Indefinite acceptation has been rejected",
    access_denied: "Access denied",
    draft_already_approved: "This finding has already been approved",
    draft_already_submitted: "This finding has already been submitted",
    draft_not_submitted: "This finding has not been submitted yet or it might've been rejected by someone else",
    draft_without_vulns: "This finding can not been approved without vulnerabilities",
    error_network: "Check your network connection",
    error_textsad: "There is an error :(",
    file_type_csv: "The file must have .csv extension",
    file_type_evidence: "The image must be .png or .gif type",
    file_type_py: "The file must have .py or .exp extension",
    file_type_wrong: "The file has an unknown or non-allowed format",
    file_type_yaml: "The file must be .yaml or .yml type",
    file_updated: "File updated ;)",
    invalid: "is invalid",
    invalid_date: "The date must be minor than six month and greater than current date",
    invalid_schema: "The uploaded file does not match the schema",
    invalid_specific: "Invalid field/line/port",
    invalid_structure: "The provided file has a wrong structure",
    invalid_treatment_mgr: "Please select a treatment manager",
    key: "Key",
    no_file_selected: "No file selected",
    no_file_update: "Failed to update the file",
    no_found: "Vulnerabilities in the request not found",
    no_verification_requested: "No verification requested",
    organization_policies: {
      exceeds_acceptance_date: "Chosen date is either in the past or exceeds the maximum number of days allowed " +
        "by the organization",
      maxium_number_of_acceptations: "Finding has been accepted the maximum number of times allowed " +
        "by the organization",
      severity_out_of_range: "Finding severity outside of the acceptance range set by the organization",
    },
    path_value: "Path value should not use backslash.",
    port_value: "Port value should be between 0 and 65535.",
    range_error: "Range limits are wrong.",
    records_removed: "Records have been removed successfully",
    report_requested: "You will be receiving a mail with the link of the report in the next minutes",
    request_remove: "Group deletion request has been sent successfully",
    title_success: "Congratulations",
    updated: "Updated",
    updated_title: "Correct!",
    value: "Value",
    verification_already_requested: "Verification already requested",
    verified_success: "This finding was marked as verified.",
    vuln_closed: "Vulnerability has already been closed",
  },
  home: {
    newGroup: {
      company: "Company",
      description: "Description",
      drills: "Include Drills Service?",
      extra_charges_may_apply: "Extra charges may apply",
      forces: "Include Forces Service?",
      integrates: "Include Integrates?",
      invalidGroup: "Invalid group name",
      name: "Group Name",
      new: {
        group: "New Group",
        text: "New",
        tooltip: "Create a new group",
      },
      noGroupName: "There are no group names available at the moment",
      success: "Group created successfully",
      switch: {
        no: "No",
        yes: "Yes",
      },
      titleSuccess: "Success",
      type: {
        continuous: "Continuous Hacking",
        one_shot: "One-Shot Hacking",
        title: "Group Type",
      },
    },
    organizations: "My Organizations",
    tagOther: "others",
    tagResume: " and {{remaining}} more",
    tags: "My Portfolios",
    title: "My Groups",
  },
  legalNotice: {
    acceptBtn: {
      text: "Accept and continue",
      tooltip: "Click if you understand and accept the terms above",
    },
    description: "Integrates, Copyright (c) 2020 Fluid Attacks. This platform contains " +
    "information property of Fluid Attacks. The client is only allowed " +
    "to use such information for documentation purposes and without disclosing " +
    "its content to third parties because it may contain ideas, concepts, prices " +
    "and/or structures property of Fluid Attacks. Its 'proprietary' " +
    "classification means that this information will only be used by those for " +
    "whom it was meant. In case of requiring total or partial reproductions they " +
    "must be done with express and written authorization of Fluid Attacks. " +
    "The rules that fundament the classification of information are " +
    "articles 72, Cartagena's agreement 344 of 1.993, article 238 of penal code " +
    "and articles 16 and its following ones from 256 law of 1.996.",
    rememberCbo: {
      text: "Remember my decision",
      tooltip: "Mark the checkbox if you want this decision to be permanent",
    },
    title: "Legal notice",
  },
  logout: "Log out",
  navbar: {
    breadcrumbRoot: "Home",
    searchPlaceholder: "Group Name",
  },
  organization: {
    tabs: {
      policies: {
        errors: {
          acceptanceSeverity: "Acceptance severity score should be a positive floating number between 0.0 and 10.0",
          acceptanceSeverityRange: "Minimum acceptance score should be lower than the maximum value",
          maxAcceptanceDays: "Maximum acceptance days should be a positive integer between 0 and 180",
          maxNumberAcceptations: "Maximum number of acceptations should be a positive integer",
        },
        policies: {
          acceptanceSeverityRange: "Temporal CVSS 3.1 score range between which a finding can be accepted",
          maxAcceptanceDays: "Maximum number of calendar days a finding can be temporally accepted",
          maxNumberAcceptations: "Maximum number of times a finding can be temporally accepted",
        },
        policy: "Policy",
        save: "Save",
        success: "Organization policies updated successfully",
        success_title: "Success",
        text: "Policies",
        tooltip: "Set common policies across all the groups of the organization",
        value: "Value",
      },
      users: {
        addButton: {
          success: "was successfully added to the organization",
          text: "Add",
          tooltip: "Add new user to the organization",
        },
        editButton: {
          text: "Edit",
          tooltip: "Edit user information",
        },
        modalAddTitle: "Add a new user to this organization",
        modalEditTitle: "Edit user information",
        removeButton: {
          success: "was successfully removed from the organization",
          text: "Remove",
          tooltip: "Remove user from the organization",
        },
        successTitle: "Success",
        text: "Users",
        tooltip: "Add and remove users from the organization",
      },
    },
  },
  registration: {
    concurrent_session_message: "You already have an active session. If you proceed, that session will " +
      "be terminated.",
    continue_as_btn: "Continue as",
    continue_btn: "Continue",
    greeting: "Hello",
    logged_in_message: "Please log out before trying to access with another account.",
    logged_in_title: "You are already logged in",
  },
  route: {
    pendingToDelete: "Group pending to delete",
  },
  search_findings: {
    acceptation_buttons: {
      approve: "Approve Acceptation",
      reject: "Reject Acceptation",
    },
    alert: {
      attention: "Attention",
    },
    critical_severity: "Critical",
    delete: {
      btn: {
        text: "Delete",
        tooltip: "Delete all about this finding",
      },
      justif: {
        duplicated: "It is duplicated",
        false_positive: "It is a false positive",
        label: "Justification",
        not_required: "Finding not required",
      },
      title: "Delete Finding",
    },
    draft_approved: "This finding was approved",
    draft_status: {
      created: "Created",
      rejected: "Rejected",
      submitted: "Submitted",
    },
    environment_table: {
      environment: "Environment",
    },
    files_table: {
      description: "Description",
      file: "File",
      upload_date: "Upload Date",
    },
    finding_deleted: "Finding {{findingId}} was deleted",
    finding_rejected: "Finding {{findingId}} was rejected",
    high_severity: "High",
    low_severity: "Low",
    medium_severity: "Medium",
    none_severity: "None",
    openVulnsLabel: "Open vulnerabilities",
    reportDateLabel: "Report date",
    repositories_table: {
      branch: "Branch",
      protocol: "Protocol",
      repository: "Repository URL",
      state: "State",
    },
    services_table: {
      active: "Active",
      continuous: "Continuous Hacking",
      deletedsoon: "Scheduled to be deleted in 1 month",
      drills: "Drills",
      errors: {
        drills_only_if_continuous: "Drills is only available in groups of type Continuous-Hacking",
        expected_group_name: "Expected: {{groupName}}",
        forces_only_if_continuous: "Forces is only available in groups of type Continuous-Hacking",
        forces_only_if_drills: "Forces is only available when Drills is too",
      },
      forces: "Forces",
      group: "Group",
      inactive: "Inactive",
      integrates: "Integrates",
      modal: {
        budget: "Budget",
        changes_to_apply: "Changes to apply",
        confirm_changes: "Confirm Changes",
        continue: "Continue",
        diff: {
          as: "as",
          from: "from",
          keep: "Keep",
          mod: "Modify",
          to: "to",
        },
        downgrading: "Please let us know the reason for downgrading your services",
        none: "None",
        observations: "Observations",
        observations_placeholder: "Please type here any observation you may have",
        other: "Other",
        project_finalization: "Project Finalization",
        project_suspension: "Project Suspension",
        title: "Change contracted services",
        type_group_name: "Please type the group name to proceed",
        warning: "Warning",
        warning_downgrade_integrates: "Disabling Integrates will schedule the group for deletion. "
          + "This will remove all of its data including findings and related vulnerabilities. "
          + "This is a destructive action and cannot be undone.",
      },
      one_shot: "One-Shot Hacking",
      oneshot: "One-Shot Hacking",
      service: "Service",
      services: "Services",
      status: "Status",
      success: "You'll receive an email shortly",
      success_title: "Services changed correctly!",
      type: "Subscription type",
    },
    severityLabel: "Severity",
    status: {
      closed: "Closed",
      open: "Open",
    },
    statusLabel: "Status",
    tab_comments: {
      tab_title: "Comments",
      tooltip: "Space where all interested parties can share information about the finding",
    },
    tab_description: {
      acceptance_date: "Temporarily accepted until",
      acceptation_justification: "Acceptation Justification",
      acceptation_user: "Acceptation User",
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
      affected_systems: {
        text: "Affected systems",
        tooltip: "Project or application that contains the vulnerability",
      },
      analyst: "Hacker",
      approval_message:
      "Remember that the indefinite acceptation of a finding requires the approval of a user with manager role",
      approval_title: "Confirmation",
      approve: "Approve",
      approve_all: "Approve all",
      approve_all_vulns: "Approve all pending vulnerabilities",
      attack_vectors: {
        text: "Impacts",
        tooltip: "Malicious actions that can be performed by exploiting the vulnerability",
      },
      bts: "External BTS",
      bts_placeholder: "https://gitlab.com/fluidattacks/integrates/-/issues/2084",
      business_criticality: "Business Criticality",
      cancel_verified: "Cancel Verify",
      cancel_verify: "Cancel Request",
      compromised_attrs: {
        text: "Compromised attributes",
        tooltip: "Type of information that can be disclosed by the vulnerability",
      },
      compromised_records: {
        text: "Compromised records",
        tooltip: "Number of records in risk",
      },
      delete: "Delete",
      deleteTags: "Delete Tags",
      delete_all: "Delete All",
      delete_all_vulns: "Delete all pending vulnerabilities",
      description: {
        text: "Description",
        tooltip: "Brief explanation of the vulnerability and how it works",
      },
      download_vulnerabilities: "Download Vulnerabilities",
      editVuln: "Edit vulnerabilites",
      editable: {
        cancel: "Cancel",
        cancel_tooltip: "Cancel changes",
        editable_tooltip: "Modify the fields of the finding",
        text: "Edit",
      },
      errorFileVuln: "Vulnerabilities file has errors",
      field: "Field",
      inputs: "Inputs",
      is_new: "New",
      line: "Line",
      line_plural: "Lines",
      mark_verified: {
        text: "Verify vulnerabilities",
        tooltip: "Assess whether the vulnerability was fixed or not in the current cycle",
      },
      mark_verified_finding: "Verify finding",
      new: "New",
      old: "Old",
      path: "Path",
      port: "Port",
      port_plural: "Ports",
      recommendation: {
        text: "Recommendation",
        tooltip: "General suggestion to solve the vulnerability",
      },
      remediation_modal: {
        justification: "Which was the applied solution?",
        message: "Verification will be requested for {{vulns}} vulnerabilities",
        observations: "What observations do you have?",
        title_observations: "Observations",
        title_request: "Justification",
      },
      request_verify: {
        text: "Reattack",
        tooltip: "Request a new reattack cycle when the vulnerability is solved",
      },
      requirements: {
        text: "Requirements",
        tooltip: "Rules that are broken and lead to the existence of the vulnerability",
      },
      risk: "Risk",
      save: {
        text: "Save",
        tooltip: "Save changes",
      },
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
      state: "State",
      tab_title: "Description",
      tag: "Tags",
      threat: {
        text: "Threat",
        tooltip: "Actor and scenery where the vulnerability can be exploited",
      },
      title: {
        text: "Title",
        tooltip: "Finding number and name",
      },
      tooltip: "Overall information about the finding: explanation, location, impacts, and threats",
      treatment: {
        accepted: "Temporarily accepted",
        accepted_undefined: "Eternally accepted",
        approved_by: "Approved by",
        in_progress: "In progress",
        new: "New",
        pending_approval: " (Pending approval)",
        rejected: "Rejected",
        title: "Treatment",
      },
      treatment_date: "Treatment Date",
      treatment_historic: "Historic Treatment",
      treatment_just: "Treatment justification",
      treatment_mgr: "Treatment manager",
      type: {
        hygiene: "Hygiene",
        security: "Security",
        title: "Finding type",
      },
      update_vulnerabilities: "Update Vulnerabilities",
      verification: "Verification",
      vulnDeleted: "Vulnerability deleted",
      vuln_approval: "Vulnerability approval status was changed",
      weakness: {
        text: "Weakness",
        tooltip: "Related Common Weakness Enumeration (CWE) according to MITRE",
      },
      where: "Where",
    },
    tab_events: {
      affectation: "Affectation",
      affected_components: "Affected components",
      analyst: "Hacker",
      client: "Client",
      closing_date: "Closing date",
      comments: "Comments",
      date: "Date",
      description: "Description",
      edit: "Edit",
      event_in: "Event present in",
      evidence: "Evidence",
      fluid_group: "Fluid Attacks' Group",
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
        det_attack: "Client detects an attack",
        high_approval: "High availability approval",
        inacc_ambient: "Inaccessible environment",
        incor_supplies: "Incorrect or missing supplies",
        other: "Other",
        toe_differs: "ToE different from what was agreed upon",
        uns_ambient: "Unstable ambient",
      },
    },
    tab_evidence: {
      animation_exploit: "Exploitation animation",
      detail: "Detail",
      editable: "Edit",
      evidence_exploit: "Exploitation evidence",
      remove: "Delete",
      tab_title: "Evidence",
      tooltip: "Images or animation representing the exploitation process to support the existence of the finding",
      update: "Update",
    },
    tab_exploit: {
      tab_title: "Exploit",
      tooltip: "Script to replicate the exploitation process using Asserts",
    },
    tab_indicators: {
      authors: "Current month authors",
      cancelDeletion: "Cancel deletion",
      cancelGroupDeletion: "Cancel group deletion",
      closed: "Closed",
      closed_percentage: "Closed vulnerabilities",
      commits: "Current month commits",
      data_chart_accepted_closed: "Accepted + Closed",
      data_chart_closed: "Closed",
      data_chart_found: "Found",
      data_chart_legend_vulnerabilities: "Vulnerabilities",
      data_chart_legend_week: "Weeks",
      days: "days",
      forces: {
        builds: "builds",
        indicators: {
          builds: {
            accepted_risk: {
              desc: "Security issues your team decided to live with",
              title: "Builds with accepted risk",
            },
            allowed: {
              desc: "Protect them by enabling the Strict mode",
              title: "Vulnerable builds",
              total: "have security issues",
            },
            stopped: {
              desc: "Vulnerable code that never saw the light",
              title: "Protected builds",
            },
          },
          has_forces: {
            protected: "Protected by Forces",
            protected_desc: "Forces helps you build a safe system",
            title: "System status",
            unprotected: "Not protected by Forces",
            unprotected_desc: "Vulnerable code may be deployed to production",
          },
          service_use: {
            title: "Service usage",
            total: "times",
          },
          strictness: {
            strict: "Strict",
            strict_desc: "Strict mode forces the fix of security issues",
            title: "Ratio of builds in Strict mode",
          },
        },
        sub_title: "Last 7 days",
        title: "Forces Indicators",
      },
      git_title: "Git Indicators",
      groupIsRemoving: "This group is expected to be removed on <strong>{{deletionDate}}</strong>" +
        "<br />Requested by <strong>{{userEmail}}</strong>",
      group_title: "Group Indicators",
      last_closing_vuln: {
        text: "Days since last closed vulnerability",
        tooltip: "Last time you fixed a vulnerability",
      },
      max_open_severity: "Max open severity",
      max_severity: "Max severity found",
      mean_remediate: {
        text: "Mean time to remediate",
        tooltip: "Amount of time it will takes your development team to fix a vulnerability",
      },
      open: "Open",
      pending_closing_check: {
        text: "Pending closing verification",
        tooltip: "Number of vulnerabilities you addressed and are pending for Fluid Attacks validation",
      },
      repositories: "Analyzed Repositories",
      status_graph: "Status",
      success: "Group deletion was cancelled successfully",
      tags: {
        modal_title: "Add tags information",
      },
      total_findings: {
        text: "Total Findings",
        tooltip: "Number of types of vulnerabilities that you have",
      },
      total_vulnerabilitites: {
        text: "Total Vulnerabilities",
        tooltip: "Number of times that the total findings types repeat within your system",
      },
      treatment_accepted: "Temporarily accepted",
      treatment_accepted_undefined: "Eternally accepted",
      treatment_graph: "Treatment",
      treatment_in_progress: "In progress",
      treatment_no_defined: "Not defined",
      undefined_treatment: {
        text: "Open vulnerabilities with no defined treatment",
        tooltip: "Number of vulnerabilities that have a default treatment setting",
      },
    },
    tab_observations: {
      tab_title: "Observations",
      tooltip: "Space to review the finding and suggest adjustments. For internal purposes only",
    },
    tab_records: {
      tab_title: "Records",
      tooltip: "Information that will be compromised or disclosed by exploiting the vulnerability",
    },
    tab_resources: {
      add_repository: "Add",
      base_url_placeholder: "gitlab.com/fluidattacks/integrates.git",
      branch: {
        label: "Branch",
        tooltip: "Target branch",
      },
      branch_placeholder: "master",
      cannotRemove: "Cannot remove group, permission denied",
      change_state: "Change state",
      description: "Description",
      download: "Download",
      environment: {
        btn_tooltip: "Add environments",
        text: "Environment",
      },
      environments_title: "Environments",
      files: {
        btn_tooltip: "Add a file",
        title: "Files",
      },
      groupToRemove: "Please type: <strong>{{projectName}}</strong>, to proceed",
      https: "HTTPS",
      invalid_chars: "File name has invalid characters.",
      modal_env_title: "Add environment information",
      modal_file_title: "Add file",
      modal_options_content: "What do you want to do with the file ",
      modal_options_title: "File options",
      modal_plus_btn: {
        tooltip: "Add another repository",
      },
      modal_repo_title: "Add repository information",
      modal_trash_btn: {
        tooltip: "Remove information about this repository",
      },
      no_file_upload: "Failed to upload the file",
      no_selection: "You must select an item from the table.",
      protocol: {
        label: "Protocol",
        tooltip: "Data transfer protocol",
      },
      removeGroup: "Delete Group",
      remove_repository: "Remove",
      repeated_input: "There are repeated values in the form",
      repeated_item: "One or more items to add exist already.",
      repositories: {
        add_tooltip: "Add repositories",
        title: "Repositories",
      },
      repository: {
        label: "Repository URL",
        tooltip: "Repository URL according to the protocol",
      },
      ssh: "SSH",
      success: "Item added successfully.",
      success_change: "Item state changed successfully.",
      success_remove: "Item removed successfully.",
      tags: {
        add_tooltip: "Add a portfolio",
        remove_tooltip: "Remove selected portfolio",
        title: "Portfolio",
      },
      total_envs: "Total environments: ",
      total_files: "Total files: ",
      total_repos: "Total repositories: ",
      uploading_progress: "Uploading file...",
      warningMessage: "Deleting the group will remove its findings and related vulnerabilities." +
        "<br /> Deleted groups cannot be restored.",
    },
    tab_severity: {
      attack_complexity: {
        text: "Attack Complexity",
        tooltip: "Conditions beyond the attacker’s control that must exist in order to exploit the vulnerability",
      },
      attack_complexity_options: {
        high: "High",
        low: "Low",
      },
      attack_vector: {
        text: "Attack Vector",
        tooltip: "Context by which vulnerability exploitation is possible",
      },
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
      availability_impact: {
        text: "Availability Impact",
        tooltip: "Availability refers to the accessibility of information resources",
      },
      availability_impact_options: {
        high: "High",
        low: "Low",
        none: "None",
      },
      availability_options: {
        complete: "Complete: There is a completely down target",
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
        high_complex: "High: Special conditions such as administrative access are required",
        low_complex: "Low: No special conditions are required",
        medium_complex: "Medium: Some conditions such as system access are required",
      },
      confidence: "Confidence Level",
      confidence_options: {
        confirmed: "Confirmed: The vulnerability is recognized by the manufacturer",
        not_confirm: "Not confirmed: There are few sources that recognize vulnerability",
        not_corrob: "Not corroborated: Vulnerability is recognized by unofficial sources",
      },
      confidentiality: "Confidentiality Impact",
      confidentiality_impact: {
        text: "Confidentiality Impact",
        tooltip: "Confidentiality refers to limiting information access and disclosure to only authorized users, " +
          "as well as preventing access by, or disclosure to, unauthorized ones",
      },
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
      exploitability: {
        text: "Exploitability",
        tooltip: "Likelihood of the vulnerability being attacked",
      },
      exploitability_options: {
        conceptual: "Conceptual: There are laboratory tests",
        functional: "Functional: There is an exploit",
        high: "High: Exploit is not required or it can be automated",
        improbable: "Improbable: There is no exploit",
        proof_of_concept: "Proof of Concept",
        unproven: "Unproven",
      },
      integrity: "Integrity Impact",
      integrity_impact: {
        text: "Integrity Impact",
        tooltip: "Integrity refers to the trustworthiness and veracity of information",
      },
      integrity_impact_options: {
        high: "High",
        low: "Low",
        none: "None",
      },
      integrity_options: {
        complete: "Complete: Posibility to modify all target information",
        none: "None: There is no impact",
        partial: "Partial: Posibility to modify some target information",
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
      privileges_required: {
        text: "Privileges Required",
        tooltip: "Level of privileges an attacker must possess before successfully exploiting the vulnerability",
      },
      privileges_required_options: {
        high: "High",
        low: "Low",
        none: "None",
      },
      remediation_level: {
        text: "Remediation Level",
        tooltip: "State of art of the current vulnerability",
      },
      remediation_level_options: {
        official_fix: "Official Fix",
        temporary_fix: "Temporary Fix",
        unavailable: "Unavailable",
        workaround: "Workaround",
      },
      report_confidence: {
        text: "Report Confidence",
        tooltip: "Degree of confidence in the existence of the vulnerability " +
          "and the credibility of the known technical details",
      },
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
      severity_scope: {
        text: "Scope",
        tooltip: "Impacts to the resources beyond the security scope",
      },
      severity_scope_options: {
        changed: "Changed",
        unchanged: "Unchanged",
      },
      solve: "Mark as solved",
      tab_title: "Severity",
      tooltip: "Assigned score according to CVSS 3.1 metrics",
      update: "Update",
      user_interaction: {
        text: "User Interaction",
        tooltip: "Requirement for a human user, other than the attacker, to participate in the successful compromise " +
          "of the vulnerable component",
      },
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
      found: "Found",
      open: "Open",
      pending: "Pending",
      tab_title: "Tracking",
      tooltip: "Evolution of the finding over time: historical records, open/closed vulnerabilities, " +
        "and effectiveness of the solution in reattacks",
    },
    tab_users: {
      add_button: {
        text: "Add",
        tooltip: "Add a user to this group",
      },
      days_ago: "{{count}} day ago",
      days_ago_plural: "{{count}} days ago",
      edit_button: {
        text: "Edit",
        tooltip: "Select a user and edit their information",
      },
      edit_user_title: "Edit user information",
      hours_ago: "{{count}} hour ago",
      hours_ago_plural: "{{count}} hours ago",
      minutes_ago: "{{count}} minute ago",
      minutes_ago_plural: "{{count}} minutes ago",
      months_ago: "{{count}} month ago",
      months_ago_plural: "{{count}} months ago",
      no_selection: "You must select an email from the table.",
      remove_user_button: {
        text: "Remove",
        tooltip: "Remove an user from the group, first select one",
      },
      success: " now has access to this group.",
      success_admin: "User information updated.",
      success_delete: " was removed from this group.",
      textbox: "Enter the email of the person you wish to add, it must be " +
        "an Office 365 or Google email",
      title: "Add user to this group",
      title_success: "Congratulations",
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
    reports: "Reports",
    token: {
      text: "Token",
      tooltip: "Get an Integrates API Token",
    },
    user: {
      text: "Add User",
      tooltip: "Add a user",
    },
  },
  tag_indicator: {
    critical_severity: "Critical Severity",
    findings_group: "Findings by group",
    high_severity: "High Severity",
    low_severity: "Low Severity",
    mean_remediate: "Mean (average) days to remediate",
    medium_severity: "Medium Severity",
    open_findings_group: "Open findings by group",
    open_vuln: "open vulns.",
    open_vulns_groups: "Open vulnerabilities by group",
    remediated_accepted_vuln: "How many vulnerabilities are remediated and accepted?",
    remediated_vuln: "How many vulnerabilities are remediated (closed)?",
    total_vuln: "vulnerabilities",
    undefined_title: "Treatmentless by group",
    undefined_vuln: "undefined",
    vulns_groups: "Vulnerabilities by group",
  },
  update_access_token: {
    access_token: "Personal Access Token",
    close: "Close",
    copy: {
      copy: "Copy",
      failed: "It cannot be copied",
      success: "Token copied",
      successfully: "Token copied successfully",
    },
    delete: "Token invalidated successfully",
    expiration_time: "Expiration date",
    invalid_exp_time: "Expiration time must be minor than six month and greater than current date",
    invalidate: "Revoke current token",
    invalidated: "Invalidated token",
    message: "Please save this access token in a safe location. You will not be able to see it again after closing " +
    "this dialog.",
    success: "Updated access token",
    successfully: "Token updated successfully",
    title: "Update access token",
    token_created: "Token created at: ",
  },
  userModal: {
    emailPlaceholder: "someone@domain.com",
    emailText: "Enter the email of the person you wish to add, it must be " +
    "an Office 365 or Google email",
    organization: "Organization",
    phoneNumber: "Phone Number",
    responsibility: "Responsibility",
    responsibilityPlaceholder: "Product Owner, Group Manager, " +
      "Tester, ...",
    role: "Role",
    roles: {
      admin: "Admin",
      analyst: "Analyst",
      closer: "Closer",
      customer: "User",
      customeradmin: "User Manager",
      executive: "Executive",
      group_manager: "Group Manager",
      internal_manager: "Manager",
      resourcer: "Resourcer",
      reviewer: "Reviewer",
    },
    success: "{{email}} was added successfully",
  },
  validations: {
    alphanumeric: "Only alphanumeric characters",
    between: "This value must be between {{min}} and {{max}}",
    datetime: "The datetime format is not valid",
    draftTitle: "The title format is not valid",
    email: "The email format is not valid",
    file_size: "The file size must be less than {{count}}MB",
    fluid_attacks_staff_without_fluid_attacks_service:
      "Groups without an active Fluid Attacks service "
      + "can not have Fluid Attacks staff",
    greater_date: "The date must be today or before",
    infectedFile: "Our system detected that the uploaded file is infected",
    invalidCommentParent: "The comment parent is invalid",
    invalidEmailInField: "The email address inserted is not valid",
    invalidPhoneNumberInField: "The phone number inserted is not valid",
    invalidTextBeginning: "Field cannot begin with the followng character: {{ chars }}",
    invalidTextField: "Field cannot contain the following characters: {{chars}}",
    invalidUrlField: "URL value cannot contain the following characters: {{chars}}",
    invalidValueInField: "The value inserted in one of the fields is not valid",
    invalid_char: "Invalid characters, use: alphanumerics, spaces and punctuations",
    lower_date: "Invalid date",
    maxLength: "This field requires less than {{count}} characters",
    minLength: "This field requires at least {{count}} characters",
    no_fluid_attacks_hackers_in_fluid_attacks_service:
      "Groups with any active Fluid Attacks service "
      + "can only have Hackers provided by Fluid Attacks",
    numeric: "This field can only contain numbers",
    required: "Required field",
    some_required: "Select at least one value",
    tags: "This field can only contain alphanumeric characters and dashes",
    valid_date: "The date must be below six months",
    valid_date_token: "The date must be below six months",
  },
};

export = enTranslations;

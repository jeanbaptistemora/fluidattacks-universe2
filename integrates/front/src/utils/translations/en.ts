import type { ResourceKey } from "i18next";

export const enTranslations: ResourceKey = {
  analytics: {
    disjointForceDirectedGraph: {
      whereToFindings: {
        footer: {
          grey: "Each grey dot represents a resource (IP, URL, or repository).",
          redAndGreen:
            "Red and green dots represent the open and closed findings for that system, respectively.",
          size:
            "Size and darkness are proportional to the security impact on that system.",
        },
        title: "Systems Risk",
      },
    },
    emptyChart: {
      text: "Your data will be available soon!",
    },
    gauge: {
      forcesBuildsRisk: {
        footer: {
          intro:
            "Risk is proportional to the number of vulnerable changes introduced into your system:",
          preventedVulnerableBuilds:
            "Forces in strict mode stops those security issues from " +
            "being delivered to your end users.",
          vulnerableBuilds:
            "A build is considered vulnerable if it contains security issues.",
        },
        title: "Builds risk",
      },
      forcesSecurityCommitment: {
        footer: {
          acceptedRisk:
            "However, accepted vulnerabilities on Integrates are ignored by the strict mode, " +
            "and Forces will (by decision of your team) allow them to be built or deployed.",
          conclusion:
            "The maximum benefit is reached when the accepted risk is low, and the strict mode high.",
          intro:
            "Forces objective is to help your team overcome security vulnerabilities. " +
            "For this to work, we put two things in your hands:",
          strictMode:
            "The strict mode (which is enabled by default) helps you stop builds or deployments " +
            "if there are open vulnerabilities, and thus protects your system from vulnerable code introduction.",
        },
        title: "Your commitment towards security",
      },
      severity: {
        footer:
          "Security vulnerabilities are ranked based on C.V.S.S. v3.1. " +
          "The higher the score, " +
          "the more damage an attack can make to your system, " +
          "and the easier it is to carry it on",
        title: "Severity",
      },
    },
    heatMapChart: {
      findingsByTag: "Finding by tags",
      groupsByTag: "Tags by groups",
    },
    limitData: {
      all: "All",
      ninetyDays: "90",
      thirtyDays: "30",
    },
    pieChart: {
      resources: {
        footer: {
          environments:
            "Environment: A URL or IP pointing to an instance of your system.",
          final:
            "The maximum benefit is reached when every environment has" +
            " its full source-code available for us to test it.",
          intro: "Resources can be of two types: Repository and Environment.",
          repositories:
            "Repository: The associated source-code of the environment " +
            "and (ideally) its infrastructure.",
        },
        title: "Active resources distribution",
      },
      status: {
        footer: {
          intro:
            "Ratio between open and closed vulnerabilities, ignoring treatments.",
        },
        title: "Vulnerabilities status",
      },
      treatment: {
        footer: {
          accepted:
            "Temporarily accepted: A manager decided to coexist with the risk temporarily.",
          eternally:
            "Eternally accepted: A vulnerability that will never be remediated.",
          inProgress:
            "In progress: The system is currently being hardened by your developers.",
          intro:
            "In Integrates, you can plan and manage the remediation of security findings:",
          notDefined:
            "Not defined: New vulnerabilities go here until one of your managers generates an action plan.",
        },
        title: "Vulnerabilities treatment",
      },
    },
    sections: {
      extras: {
        download: "Download",
        frequencies: {
          action: {
            daily: "Subscribe daily",
            hourly: "Subscribe hourly",
            monthly: "Subscribe monthly",
            never: "Unsubscribe me",
            weekly: "Subscribe weekly",
          },
          statement: {
            daily: "Subscribed daily",
            hourly: "Subscribed hourly",
            monthly: "Subscribed monthly",
            never: "Unsubscribed",
            weekly: "Subscribed weekly",
          },
        },
        frequenciesArrivalTime: {
          daily: "Every day at 6:00 AM (America/EST)",
          hourly: "Every hour",
          monthly: "First day of each month at 6:00 AM (America/EST)",
          never: "You won't receive reports",
          weekly: "Mondays at 6:00 AM (America/EST)",
        },
        subscribedSuccessfully: {
          msg: "You'll receive an e-mail shortly",
          title: "You've been successfully subscribed!",
        },
        unsubscribedSuccessfully: {
          msg: "No more e-mails will be sent",
          title: "You've been successfully unsubscribed!",
        },
      },
      forces: {
        title: "DevSecOps",
      },
    },
    stackedBarChart: {
      riskOverTime: {
        footer: {
          accepted:
            "Open vulnerabilities with accepted treatment are exactly like open ones" +
            ", except that you decided to coexist with that risk.",
          closed:
            "Closed vulnerabilities may be seen as security breaches that your system no longer has.",
          intro:
            "In Integrates, you can track the evolution of your systems from a security point of view:",
          opened:
            "Open vulnerabilities represent a risk currently impacting your end-users and systems.",
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
        footer:
          "Once your team has solved a vulnerability you can request a re-attack. " +
          "In the re-attack process a hacker will replay the attack vector and confirm that " +
          "the proposed solution actually shields your system. " +
          "In case it does not, your team will be notified and the finding kept open.",
        title: "Findings being re-attacked",
      },
      forcesAutomatizedVulns: {
        footer:
          "Forces performs security testing of your source-code, deployed environment and infrastructure. " +
          "Single units of security problems found are displayed here.",
        title: "Automatized Vulnerabilities",
      },
      forcesRepositoriesAndBranches: {
        footer:
          "You can run Forces in any of your repositories at any of its versions (commits or branches).",
        title: "Repositories and branches",
      },
      forcesStatus: {
        footer: {
          breaks:
            "In case Forces finds one vulnerability to be open, " +
            "we can (optionally) mark the build as failed, so you never introduce known vulnerabilities " +
            "into the production environment.",
          intro:
            "By enabling Forces you get access to a Docker container built to specifically verify the status " +
            "of security findings in your system. " +
            "You can embed this container in your Continuous Integration system to test " +
            "for changes in security vulnerabilities:",
          smart:
            "Forces is fast and automatic, but it is created by the same intelligence " +
            "of the hackers who already know your system in-depth, and therefore can verify the " +
            "attack vectors that no other tool can.",
          stats:
            "Statistics from over a hundred different systems show that Forces increases the " +
            "remediation ratio, helping you to build a safer system and to be more cost-effective " +
            "throughout your Software Security Development Life Cycle.",
        },
        title: "Service status",
      },
      forcesUsage: {
        footer:
          "Number of times your team used Forces to check for vulnerabilities.",
        title: "Service usage",
      },
      meanTimeToRemediate: {
        footer:
          "Amount of time (in days) it takes to your team to fix a security vulnerability.",
        title: "Mean time to remediate (all vulnerabilities)",
      },
      meanTimeToRemediateNonTreated: {
        footer:
          "Amount of time (in days) it takes to your team to fix a security vulnerability, " +
          "excluding accepted vulnerabilities.",
        title: "Mean time to remediate (non treated vulnerabilities)",
      },
      totalFindings: {
        footer:
          "A finding is a group of vulnerabilities on your system " +
          "related to the same attack vector.",
        title: "Total findings",
      },
      totalVulnerabilities: {
        footer:
          "Vulnerabilities are the minimum units of risk. " +
          "They are tied to a system, and a specific location within that system.",
        title: "Total vulnerabilities",
      },
      vulnsWithUndefinedTreatment: {
        footer:
          "Number of vulnerabilities without a remediation plan specified by one of your managers.",
        title: "Vulnerabilities with not-defined treatment",
      },
    },
  },
  comments: {
    editorPlaceholder: "Add your comment here",
    noComments: "No comments",
    orderBy: {
      label: "Order by",
      newest: "Newest",
      oldest: "Oldest",
    },
    reply: "Reply",
    send: "Comment",
  },
  configuration: {
    close: "Close",
    confirm: "Save",
    digest: {
      label: "Daily digest (all your groups):",
      subscribed: "Yes",
      tooltip: "Daily stats from the groups you are subscribed to",
      unsubscribed: "No",
    },
    errorText: "An error occurred with your configuration",
    title: "Configuration",
  },
  confirmmodal: {
    cancel: "Cancel",
    message: "Are you sure?",
    proceed: "Proceed",
    titleCvssv2: "Update CVSSv2",
    titleGeneric: "Confirm action",
  },
  dataTableNext: {
    filters: "Filters",
    more: "--More--",
    noDataIndication: "There is no data to display",
    tooltip: "filters of search on the table",
  },
  deleteVulns: {
    notSuccess: "Vulnerability could not be eliminated",
    reportingError: "Error while reporting",
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
      groupsContributed: "Groups Contributed",
      repository: "Repository",
      tableAdvice:
        "Below you'll find the authors that have contributed " +
        "to your group in the selected month, and one example commit",
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
      errorSubmit: "Please provide {{missingFields}} before submitting",
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
      successCreate: "Draft created successfully",
      successSubmit: "Draft successfully submitted for review",
      title: "Title",
      titleSuccess: "Success",
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
        editTooltip: "Modify the evidence for this event",
        noData: "There are no evidences",
      },
      form: {
        accessibility: {
          environment: "Environment",
          repository: "Repository",
          title: "Accessibility",
        },
        actionAfter: {
          otherOther: "Execute another group of a different client",
          otherSame: "Execute another group of the same client",
          title: "Action after getting blocked",
          training: "Training",
        },
        actionBefore: {
          document: "Document group",
          testOther: "Test other part of ToE",
          title: "Action before blocking",
        },
        blockingHours: "Working hours until getting blocked",
        components: {
          clientStation: "Client's test station",
          compileError: "Compilation error",
          documentation: "Group documentation",
          fluidStation: "FLUID's test station",
          internetConn: "Internet connectivity",
          localConn: "Local connectivity (LAN, WiFi)",
          sourceCode: "Source code",
          testData: "Test data",
          title: "Affected components",
          toeAlteration: "ToE alteration",
          toeCredentials: "ToE credentials",
          toeExclusion: "ToE exclusion",
          toeLocation: "ToE location (IP, URL)",
          toePrivileges: "ToE privileges",
          toeUnaccessible: "ToE unaccessibility",
          toeUnavailable: "ToE unavailability",
          toeUnstability: "ToE unstability",
          vpnConn: "VPN connectivity",
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
        evidenceFile: "Evidence file",
        none: "None",
        other: "Other",
        responsible: "Person in charge (client)",
        type: {
          detectsAttack: "Client detects the attack",
          highAvailability: "High availability approval",
          missingSupplies: "Incorrect or missing supplies",
          specialAttack: "Authorization for special attack",
          title: "Type",
          toeChange: "Client approves ToE change",
          toeDiffers: "ToE different than agreed upon",
        },
        wrongFileType: "Evidence files must have .pdf, .zip or .csv extension",
        wrongImageType:
          "Evidence images must have .gif/.png extension for animation" +
          "/exploitation and .png for evidences",
      },
      new: "New Event",
      successCreate: "Event created successfully",
      titleSuccess: "Success",
    },
    findings: {
      boolean: {
        False: "No",
        True: "Yes",
      },
      description: {
        exploitable: "Exploitable:",
        firstSeen: "First seen:",
        lastReport: "Last report:",
        reattack: "Pending reattack",
        title: "Description",
        value: "{{count}} day ago",
        valuePlural: "{{count}} days ago",
      },
      evidence: {
        edit: "Edit",
        noData: "There are no evidences",
      },
      exportCsv: {
        text: "Export",
        tooltip: "Export to a comma-separated values file",
      },
      helpLabel: "Click on a finding to see more details",
      records: {
        noData: "There are no records",
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
        data: "  Export",
        dataTooltip:
          "Receive a zip file containing the exported data of all the findings " +
          "of this group",
        modalClose: "Close",
        modalTitle: "Reports",
        pdf: "  Executive",
        pdfTooltip:
          "Receive a pdf file with an executive report that gives you summarized information " +
          "about all the findings of this group",
        techDescription:
          "Reports are created on-demand and are protected by a <strong>passphrase</strong>. " +
          "The <strong>passphrase</strong> is generated randomly and will be " +
          "sent through a notification to your mobile device.",
        xls: "  Technical",
        xlsTooltip:
          "Receive an xls file with a technical report that gives you more detailed " +
          "information about all the findings of this group",
      },
      tableSet: {
        btn: {
          text: "Columns",
          tooltip: "Choose the fields you want to display",
        },
        modalTitle: "Columns Filter",
      },
    },
    forces: {
      compromisedToe: {
        exploitability: "Exploitability",
        status: "Status",
        title: "Compromised Surface",
        type: "Type",
        what: "What",
        where: "Where",
      },
      date: "Date",
      executionDetailsModal: {
        close: "Close",
        title: "Execution Details",
      },
      foundVulnerabilities: {
        accepted: "Accepted",
        exploitable: "Exploitable",
        notExploitable: "Not exploitable",
        title: "Vulnerabilities",
        total: "Total",
      },
      foundVulnerabilitiesNew: {
        accepted: "Accepted",
        closed: "Closed",
        open: "Open",
        title: "Vulnerabilities",
        total: "Total",
      },
      gitRepo: "Git Repository",
      identifier: "Identifier",
      kind: {
        all: "ALL",
        dynamic: "DAST",
        other: "ALL",
        static: "SAST",
        title: "Type",
      },
      status: {
        accepted: "Accepted",
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
      tableAdvice: "Click on an execution to see more details",
      tabs: {
        log: {
          text: "Execution Log",
          tooltip: "Log record of the execution of forces in YAML format",
        },
        summary: {
          text: "Summary",
          tooltip: "Status summary of found vulnerabilities",
        },
      },
    },
    scope: {
      common: {
        add: "Add new root",
        addTooltip: "Add a new git root to this group",
        confirm: "Confirm state change",
        deactivation: {
          other: "Which?",
          reason: {
            label: "Reason",
            mistake: "Registered by mistake",
            moved: "Moved to another root",
            other: "Other",
            scope: "Out of scope",
          },
          title: "Deactivate Root",
        },
        edit: "Edit root",
        editTooltip: "Edit the selected git root",
        errors: {
          duplicateNickname:
            "An active root with the same Nickname already exists " +
            "please type a new nickname",
          duplicateUrl:
            "An active root with the same URL/Branch already exists " +
            "within the organization",
          hasOpenVulns:
            "There are open vulnerabilities reported for this root. " +
            "Attend them first and try again",
        },
        lastCloningStatusUpdate: "Last status update",
        lastStateStatusUpdate: "Last state update",
        state: "State",
      },
      git: {
        envUrls: "Environment URLs",
        errors: {
          invalid: "Repository URL or branch are not valid",
          rootInGitignore:
            "Root name should not be included in gitignore pattern",
        },
        filter: {
          documentation:
            "https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitignore.html#_pattern_format",
          exclude: "Gitignore",
          placeholder: "**/example.txt",
          title: "Filters",
          tooltip:
            "Patterns that define which files should be ignored during the analysis",
          warning:
            "Vulnerabilities of various impact can exist in test directories. " +
            "We recommend you do not exclude any part of your repository. " +
            "Decide at your own risk.",
        },
        healthCheck: {
          accept: "I accept the additional costs derived from the healthcheck",
          confirm: "Would you like a health check for the existing code?",
          title: "Health Check",
        },
        manageEnvs: "Manage environments",
        manageEnvsTooltip:
          "Add, edit or remove environment URLs for the selected git root",
        repo: {
          branch: "Branch",
          cloning: {
            message: "Message",
            status: "Status",
          },
          environment: "Environment kind",
          environmentHint: "(Production, QA or other)",
          nickname: "Nickname",
          nicknameHint:
            "Nickname must be unique and different from the repository name",
          title: "Git repository",
          url: "URL",
        },
        title: "Git Roots",
      },
      ip: {
        address: "Address",
        port: "Port",
        title: "IP Roots",
      },
      url: {
        host: "Host",
        path: "Path",
        port: "Port",
        protocol: "Protocol",
        title: "URL Roots",
      },
    },
    tabs: {
      analytics: {
        text: "Analytics",
        tooltip: "Group status at a glance",
      },
      authors: {
        text: "Authors",
        tooltip: "People that have contributed to your group",
      },
      comments: {
        scope: {
          external: "#external",
          internal: "#internal",
        },
        text: "Consulting",
        tooltip:
          "Space where all interested parties can share information about the group",
      },
      drafts: {
        text: "Drafts",
        tooltip: "Add new findings and review those yet to be approved",
      },
      events: {
        text: "Events",
        tooltip:
          "Keep track of all the situations that are affecting the group",
      },
      findings: {
        text: "Vulnerabilities",
        tooltip: "Keep track of the status of all the approved findings",
      },
      forces: {
        text: "DevSecOps",
        tooltip: "Check the state of the Forces jobs in your CI/CD",
      },
      indicators: {
        text: "Analytics",
        tooltip: "Summary of the group status",
      },
      resources: {
        text: "Scope",
        tooltip:
          "Configure the resources needed by the security tests and the services to be purchased," +
          " if applicable",
      },
      toe: {
        text: "ToE",
        tooltip: "Target of evaluation",
      },
      users: {
        text: "Stakeholders",
        tooltip: "Add, edit, and remove users from this group",
      },
    },
    toe: {
      inputs: {
        commit: "Commit",
        component: "Component",
        createdDate: "Seen at",
        entryPoint: "Entry point",
        seenFirstTimeBy: "Seen first time by",
        testedDate: "Attack moment",
        verified: "Attacked",
        vulns: "Vulns",
      },
      lines: {
        attacked: "Attacked",
        comments: "Comments",
        coverage: "Coverage",
        filename: "Filename",
        loc: "LOC",
        modifiedCommit: "Modified commit",
        modifiedDate: "Modified date",
        no: "No",
        pendingLines: "Pending lines",
        sortsRiskLevel: "Priority (IA/ML)",
        testedDate: "Attack moment",
        testedLines: "Attacked lines",
        yes: "Yes",
      },
      tabs: {
        inputs: {
          text: "ToE Inputs",
          tooltip:
            "Track which application/infrastructure inputs have been reviewed",
        },
        lines: {
          text: "ToE Lines",
          tooltip: "Track which source code lines have been reviewed",
        },
      },
    },
  },
  groupAlerts: {
    acceptationApproved: "Indefinite acceptation has been approved",
    acceptationRejected: "Indefinite acceptation has been rejected",
    accessDenied: "Access denied",
    confirmedZeroRiskSuccess: "Zero risk vulnerability has been confirmed",
    draftAlreadyApproved: "This finding has already been approved",
    draftAlreadySubmitted: "This finding has already been submitted",
    draftNotSubmitted:
      "This finding has not been submitted yet or it might've been rejected by someone else",
    draftWithoutVulns:
      "This finding can not been approved without vulnerabilities",
    errorNetwork: "Check your network connection",
    errorTextsad: "There is an error :(",
    expiredInvitation: "The stakeholder has an expired invitation",
    fileTypeCsv: "The file must have .csv extension",
    fileTypeEvidence: "The image must be .png or .gif type",
    fileTypePy: "The file must have .py or .exp extension",
    fileTypeWrong: "The file has an unknown or non-allowed format",
    fileTypeYaml: "The file must be .yaml or .yml type",
    fileUpdated: "File updated ;)",
    invalid: "is invalid",
    invalidDate:
      "The date must be minor than six month and greater than current date",
    invalidNOfVulns: "You can upload a maximum of 100 vulnerabilities per file",
    invalidSchema: "The uploaded file does not match the schema",
    invalidSpecific: "Invalid field/line/port",
    invalidStructure: "The provided file has a wrong structure",
    invalidTreatmentMgr: "Please select a treatment manager",
    key: "Key",
    noFileSelected: "No file selected",
    noFileUpdate: "Failed to update the file",
    noFound: "Vulnerabilities in the request not found",
    noVerificationRequested: "No verification requested",
    organizationPolicies: {
      exceedsAcceptanceDate:
        "Chosen date is either in the past or exceeds the maximum number of days allowed " +
        "by the organization",
      severityOutOfRange:
        "Finding severity outside of the acceptance range set by the organization",
    },
    pathValue: "Path value should not use backslash.",
    portValue: "Port value should be between 0 and 65535.",
    rangeError: "Range limits are wrong.",
    recordsRemoved: "Records have been removed successfully",
    rejectedZeroRiskSuccess: "Zero risk vulnerability has been rejected",
    reportRequested:
      "You will be receiving a mail with the link of the report in the next minutes",
    requestRemove: "Group deletion request has been sent successfully",
    requestedZeroRiskSuccess: "Zero risk vulnerability has been requested",
    titleSuccess: "Congratulations",
    updated: "Updated",
    updatedTitle: "Correct!",
    value: "Value",
    verificationAlreadyRequested: "Verification already requested",
    verifiedSuccess: "This finding was marked as verified.",
    vulnClosed: "Vulnerability has already been closed",
    zeroRiskAlreadyRequested: "Zero risk vulnerability already requested",
    zeroRiskIsNotRequested: "Zero risk vulnerability is not requested",
  },
  legalNotice: {
    acceptBtn: {
      text: "Accept and continue",
      tooltip: "Click if you understand and accept the terms above",
    },
    description:
      "Integrates, Copyright (c) {{currentYear}} Fluid Attacks. This platform contains " +
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
  login: {
    "2fa":
      "We strongly recommend you to use 2-Step verification. For more information please visit:",
    auth: "Please authenticate to proceed.",
    bitbucket: "Sign in with Bitbucket",
    google: "Sign in with Google",
    microsoft: "Sign in with Microsoft",
    newuser: "If you are a new user, click below to sign up.",
  },
  logout: "Log out",
  navbar: {
    newsTooltip: "Latest updates about ASM",
    role: "Role:",
    searchPlaceholder: "Search Group Name",
    token: {
      text: "API",
      tooltip: "Get an Integrates API Token",
    },
  },
  organization: {
    tabs: {
      analytics: {
        text: "Analytics",
        tooltip: "Organization status at a glance",
      },
      groups: {
        disabled: "Disabled",
        enabled: "Enabled",
        newGroup: {
          description: {
            text: "Description",
            tooltip: "Brief description to identify the group",
          },
          drills: {
            text: "Include Squad Service?",
            tooltip:
              "Squad finds deep and zero-day vulnerabilities during software development",
          },
          extraChargesMayApply: "Extra charges may apply",
          forces: {
            text: "Include DevSecOps agent?",
            tooltip:
              "Changes to the target of evaluation can be continuously tested against the closing of confirmed " +
              "vulnerabilities. The agent can be included in CI/CD",
          },
          integrates: {
            text: "Include ASM?",
            tooltip:
              "Communication platform where all group stakeholders can interact",
          },
          language: {
            EN: "English",
            ES: "Spanish",
            text: "Report Language",
            tooltip: "Language in which findings should be reported",
          },
          name: "Group Name",
          new: {
            group: "New Group",
            text: "New Group",
            tooltip: "Create a new group",
          },
          noGroupName: "There are no group names available at the moment",
          organization: {
            text: "Organization",
            tooltip:
              "Name of the organization that is associated with this group",
          },
          skims: {
            text: "Include Machine service?",
            tooltip:
              "Vulnerability detection tool that scans and reports security issues in your source code",
          },
          success: "Group created successfully",
          switch: {
            no: "No",
            yes: "Yes",
          },
          titleSuccess: "Success",
          type: {
            continuous: "Continuous Hacking",
            oneShot: "One-Shot Hacking",
            title: "Group Type",
            tooltip: "Type of subscription",
          },
        },
        text: "Groups",
        tooltip: "Groups that belong to the organization",
      },
      policies: {
        errors: {
          acceptanceSeverity:
            "Acceptance severity score should be a positive floating number between 0.0 and 10.0",
          acceptanceSeverityRange:
            "Minimum acceptance score should be lower than the maximum value",
          maxAcceptanceDays:
            "Maximum acceptance days should be a positive integer between 0 and 180",
          maxNumberAcceptations:
            "Maximum number of acceptations should be a positive integer",
        },
        findings: {
          addPolicies: {
            success:
              "Remember that the aplication of the policy requires the approval of a user with manager role",
          },
          deactivatePolicies: {
            modalTitle: "Disable organization finding policy",
            success:
              "The finding policy was disabled successfully, changes will be apply it within next minutes",
          },
          errors: {
            alreadyReviewd: "The finding policy has already been reviewed",
            duplicateFinding: "The finding policy already exists",
            notFound: "Finding policy not found",
          },
          handlePolicies: {
            success: {
              approved: "The policy will be apply it within next minutes",
              rejected: "The policy was rejected successfully",
            },
          },
          tooltip: {
            addButton: "Add organization policy pending to approve",
            approveButton: "Approve organization finding policy",
            deactivateButton: "Disable organization finding policy",
            rejectButton: "Reject organization finding policy",
          },
        },
        policies: {
          acceptanceSeverityRange:
            "Temporal CVSS 3.1 score range between which a finding can be accepted",
          maxAcceptanceDays:
            "Maximum number of calendar days a finding can be temporally accepted",
          maxNumberAcceptations:
            "Maximum number of times a finding can be temporally accepted",
        },
        policy: "Policy",
        recommended: {
          acceptanceDays: "0",
          acceptanceSeverity: "0.0    -    0.0",
          numberAcceptations: "0",
          title: "Recommended Values",
        },
        save: "Save",
        success: "Organization policies updated successfully",
        successTitle: "Success",
        text: "Policies",
        tooltip:
          "Set common policies across all the groups of the organization",
        value: "Value",
      },
      portfolios: {
        remainingDescription: " and {{remaining}} more",
        table: {
          groups: "Groups",
          nGroups: "# of Groups",
          portfolio: "Portfolio",
        },
        tabs: {
          group: {
            text: "Groups",
            tooltip: "Groups that belong to the portfolio",
          },
          indicators: {
            text: "Analytics",
            tooltip: "Summary of the portfolio status",
          },
        },
        text: "Portfolios",
        tooltip:
          "Classify groups using tags and have overall indicators of those tags",
      },
      users: {
        addButton: {
          success: "was successfully added to the organization",
          text: "Add",
          tooltip: "Add new user to the organization",
        },
        editButton: {
          success: "was successfully edited",
          text: "Edit",
          tooltip: "Edit user information",
        },
        modalAddTitle: "Add a new user to this organization",
        modalEditTitle: "Edit stakeholder information",
        removeButton: {
          success: "was successfully removed from the organization",
          text: "Remove",
          tooltip: "Remove stakeholder from the organization",
        },
        successTitle: "Success",
        text: "Stakeholders",
        tooltip: "Add and remove users from the organization",
      },
    },
  },
  registration: {
    concurrentSessionMessage:
      "You already have an active session. If you proceed, that session will " +
      "be terminated.",
    concurrentSessionTitle: "Active Session Detected",
    continueAsBtn: "Continue as",
    continueBtn: "Continue",
    greeting: "Hello",
    loggedInMessage:
      "Please log out before trying to access with another account.",
    loggedInTitle: "You are already logged in",
  },
  route: {
    pendingToDelete: "Group pending to delete",
  },
  searchFindings: {
    acceptationButtons: {
      approve: "Approve Acceptation",
      reject: "Reject Acceptation",
    },
    agentTokenSection: {
      about: "Generate, reveal or update token for DevSecOps.",
      generate: "Manage Token",
      install: "Install",
      title: "DevSecOps Agent",
    },
    alert: {
      attention: "Attention",
    },
    criticalSeverity: "Critical",
    delete: {
      btn: {
        text: "Delete",
        tooltip: "Delete all about this finding",
      },
      justif: {
        duplicated: "It is duplicated",
        falsePositive: "It is a false positive",
        label: "Justification",
        notRequired: "Finding not required",
      },
      title: "Delete Finding",
    },
    discoveryDateLabel: "Discovery date",
    draftApproved: "This finding was approved",
    draftStatus: {
      created: "Created",
      rejected: "Rejected",
      submitted: "Submitted",
    },
    environmentTable: {
      environment: "Environment",
      uploadDate: "Since",
    },
    filesTable: {
      description: "Description",
      file: "File",
      uploadDate: "Since",
    },
    findingDeleted: "Finding {{findingId}} was deleted",
    findingRejected: "Finding {{findingId}} was rejected",
    highSeverity: "High",
    infoTable: {
      EN: "English",
      ES: "Spanish",
      attribute: "Attribute",
      lang: "Language",
      title: "Information",
      value: "Value",
    },
    lowSeverity: "Low",
    mediumSeverity: "Medium",
    noneSeverity: "None",
    openVulnsLabel: "Open vulnerabilities",
    repositoriesTable: {
      state: "State",
    },
    servicesTable: {
      active: "Active",
      continuous: "Continuous Hacking",
      deleteGroup: {
        deleteGroup: "Delete this group",
        typeGroupName: "Please type the group name to proceed.",
        warning: "Group deletion is a destructive action and cannot be undone.",
        warningBody:
          "This action will immediately delete the group. " +
          "This will remove all of its data including findings and related vulnerabilities. " +
          "This is a destructive action and cannot be undone.",
        warningTitle: "Warning!",
      },
      deletedsoon: "Scheduled to be deleted in 1 month",
      drills: "Squad",
      errors: {
        drillsOnlyIfContinuous:
          "Drills is only available in groups of type Continuous-Hacking",
        expectedGroupName: "Expected: {{groupName}}",
        forcesOnlyIfContinuous:
          "Forces is only available in groups of type Continuous-Hacking",
        forcesOnlyIfDrills: "Forces is only available when Drills is too",
        organizationNotExists: "Target organization does not exist",
        userNotInOrganization:
          "User is not a member of the target organization",
      },
      forces: "DevSecOps agent",
      group: "Group",
      inactive: "Inactive",
      integrates: "ASM",
      modal: {
        budget: "Budget",
        changesToApply: "Changes to apply",
        confirmChanges: "Confirm Changes",
        continue: "Continue",
        diff: {
          as: "as",
          from: "from",
          keep: "Keep",
          mod: "Modify",
          to: "to",
        },
        downgrading:
          "Please let us know the reason for downgrading your services",
        none: "None",
        observations: "Observations",
        observationsPlaceholder:
          "Please type here any observation you may have",
        other: "Other",
        projectFinalization: "Project Finalization",
        projectSuspension: "Project Suspension",
        title: "Change contracted services",
        typeGroupName: "Please type the group name to proceed",
        warning: "Warning",
        warningDowngradeIntegrates:
          "Disabling Integrates will immediately delete the group. " +
          "This will remove all of its data including findings and related vulnerabilities. " +
          "This is a destructive action and cannot be undone.",
      },
      oneShot: "One-Shot Hacking",
      oneshot: "One-Shot Hacking",
      service: "Service",
      services: "Services",
      skims: "Machine",
      status: "Status",
      success: "You'll receive an email shortly",
      successTitle: "Services changed correctly!",
      type: "Subscription type",
      unsubscribe: {
        button: "Unsubscribe",
        success: "Unsubscription from {{groupName}} was successful",
        successTitle: "Success",
        title: "Unsubscribe",
        typeGroupName: "Please type the group name to proceed.",
        warning: "Revoke access permissions to this group.",
        warningBody:
          "This action will unsubscribe you from the group. " +
          "If you do not have more groups, you will be removed from integrates. ",
        warningTitle: "Warning!",
      },
    },
    severityLabel: "Severity",
    status: {
      closed: "Closed",
      open: "Open",
    },
    statusLabel: "Status",
    tabComments: {
      tabTitle: "Consulting",
      tooltip:
        "Space where all interested parties can share information about the finding",
    },
    tabDescription: {
      acceptanceDate: "Temporarily accepted until",
      acceptationJustification: "Acceptation Justification",
      acceptationUser: "Acceptation User",
      action: "Action",
      actor: {
        anyCustomer: "Any customer of the organization",
        anyEmployee: "Any employee of the organization",
        anyInternet: "Anyone on Internet",
        anyStation: "Anyone with access to the station",
        oneEmployee: "Only one employee",
        someCustomer: "Only some customers of the organization",
        someEmployee: "Only some employees",
        title: "Actor",
      },
      affectedSystems: {
        text: "Affected systems",
        tooltip: "Project or application that contains the vulnerability",
      },
      analyst: "Hacker",
      approvalMessage:
        "Remember that the indefinite acceptation of a finding requires the approval of a user with manager role",
      approvalTitle: "Confirmation",
      approve: "Approve",
      approveAll: "Approve all",
      approveAllVulns: "Approve all pending vulnerabilities",
      attackVectors: {
        text: "Impacts",
        tooltip:
          "Malicious actions that can be performed by exploiting the vulnerability",
      },
      bts: "External BTS",
      btsPlaceholder:
        "https://gitlab.com/fluidattacks/integrates/-/issues/2084",
      businessCriticality: "Level",
      cancelVerified: "Cancel",
      cancelVerify: "Cancel",
      compromisedAttrs: {
        text: "Compromised attributes",
        tooltip:
          "Type of information that can be disclosed by the vulnerability",
      },
      compromisedRecords: {
        text: "Compromised records",
        tooltip: "Number of records in risk",
      },
      delete: "Delete",
      deleteAll: "Delete All",
      deleteAllVulns: "Delete all pending vulnerabilities",
      deleteTags: "Delete Tags",
      description: {
        text: "Description",
        tooltip: "Brief explanation of the vulnerability and how it works",
      },
      downloadVulnerabilities: "Download Vulnerabilities",
      downloadVulnerabilitiesTooltip:
        "Download a yaml file with all the vulnerabilities of this finding",
      editVuln: "Edit vulnerabilities",
      editVulnTooltip: "Modify the treatment for the selected vulnerabilities",
      editable: {
        cancel: "Cancel",
        cancelTooltip: "Cancel changes",
        editableTooltip: "Modify the fields of the finding",
        text: "Edit",
      },
      errorFileVuln: "Vulnerabilities file has errors",
      field: "Field",
      handleAcceptationModal: {
        title: "Observations",
        zeroRiskJustification: {
          confirmation: {
            fp: "FP",
            outOfTheScope: "Out of the scope",
          },
          rejection: {
            complementaryControl: "Complementary control",
            fn: "FN",
          },
        },
      },
      inputs: "Inputs",
      isNew: "New",
      line: "Line",
      linePlural: "Lines",
      markVerified: {
        text: "Verify vulnerabilities",
        tooltip:
          "Assess whether the vulnerability was fixed or not in the current cycle",
      },
      markVerifiedFinding: "Verify finding",
      new: "New",
      old: "Old",
      path: "Path",
      port: "Port",
      portPlural: "Ports",
      recommendation: {
        text: "Recommendation",
        tooltip: "General suggestion to solve the vulnerability",
      },
      remediationModal: {
        justification: "Which was the applied solution?",
        message: "Verification will be requested for {{vulns}} vulnerabilities",
        observations: "What observations do you have?",
        titleObservations: "Observations",
        titleRequest: "Justification",
      },
      requestVerify: {
        text: "Reattack",
        tooltip:
          "Request a new reattack cycle when the vulnerability is solved",
      },
      requirements: {
        text: "Requirements",
        tooltip:
          "Rules that are broken and lead to the existence of the vulnerability",
      },
      risk: "Risk",
      save: {
        text: "Save",
        tooltip: "Save changes",
      },
      scenario: {
        anonInter: "Anonymous from Internet",
        anonIntra: "Anonymous from Intranet",
        authExtra: "Authorized Extranet user",
        authInter: "Authorized Internet user",
        authIntra: "Authorized Intranet user",
        title: "Scenario",
        unauthExtra: "Unauthorized Extranet user",
        unauthInter: "Unauthorized Internet user",
        unauthIntra: "Unauthorized Intranet user",
      },
      severity: "Severity",
      sorts: {
        text: "Sorts",
        tooltip:
          "Did Sorts guide you to the file where you found the vulnerability?",
      },
      state: "State",
      tabTitle: "Description",
      tag: "Tags",
      threat: {
        text: "Threat",
        tooltip: "Actor and scenery where the vulnerability can be exploited",
      },
      title: {
        text: "Title",
        tooltip: "Finding number and name",
      },
      tooltip:
        "Overall information about the finding: explanation, location, impacts, and threats",
      treatment: {
        accepted: "Temporarily accepted",
        acceptedUndefined: "Eternally accepted",
        approvedBy: "Approved by",
        confirmZeroRisk: "Confirm zero risk",
        inProgress: "In progress",
        new: "New",
        pendingApproval: " (Pending approval)",
        rejectZeroRisk: "Reject zero risk",
        rejected: "Rejected",
        requestZeroRisk: "Request zero risk",
        title: "Treatment",
      },
      treatmentDate: "Treatment Date",
      treatmentHistoric: "Historic Treatment",
      treatmentJust: "Treatment justification",
      treatmentMgr: "Treatment manager",
      type: {
        hygiene: "Hygiene",
        security: "Security",
        title: "Finding type",
      },
      updateVulnerabilities: "Update Vulnerabilities",
      updateVulnerabilitiesTooltip:
        "Modify the existing vulnerabilities using the selected yaml file",
      verification: "Verification",
      vulnApproval: "Vulnerability approval status was changed",
      vulnBatchLimit: "You can update up to {{count}} vulnerabilities at once",
      vulnDeleted: "Vulnerability deleted",
      weakness: {
        text: "Weakness",
        tooltip: "Related Common Weakness Enumeration (CWE) according to MITRE",
      },
      where: "Where",
      zeroRisk: "Zero risk",
    },
    tabEvents: {
      affectation: "Affectation",
      affectedComponents: "Affected components",
      analyst: "Hacker",
      client: "Client",
      closingDate: "Closing date",
      comments: "Comments",
      date: "Date",
      description: "Description",
      edit: "Edit",
      eventIn: "Event present in",
      evidence: "Evidence",
      fluidGroup: "Fluid Attacks' Group",
      id: "ID",
      resume: "Resume",
      status: "Status",
      statusValues: {
        solve: "Solved",
        unsolve: "Unsolved",
      },
      tableAdvice: "Click on an event to see more details",
      type: "Type",
      typeValues: {
        approvChange: "Client approves the change of ToE",
        authAttack: "Authorization for special attack",
        detAttack: "Client detects an attack",
        highApproval: "High availability approval",
        inaccAmbient: "Inaccessible environment",
        incorSupplies: "Incorrect or missing supplies",
        other: "Other",
        toeDiffers: "ToE different from what was agreed upon",
        unsAmbient: "Unstable ambient",
      },
    },
    tabEvidence: {
      animationExploit: "Exploitation animation",
      date: "Date: ",
      descriptionTooltip: "Brief explanation about the evidence",
      detail: "Detail",
      editable: "Edit",
      editableTooltip: "Modify the evidence for this finding",
      evidenceExploit: "Exploitation evidence",
      remove: "Delete",
      removeTooltip: "Delete this evidence",
      tabTitle: "Evidence",
      tooltip:
        "Images or animation representing the exploitation process to support the existence of the finding",
      update: "Update",
      updateTooltip: "Update all modified evidences",
    },
    tabIndicators: {
      authors: "Current month authors",
      cancelDeletion: "Cancel deletion",
      cancelGroupDeletion: "Cancel group deletion",
      closed: "Closed",
      closedPercentage: "Closed vulnerabilities",
      commits: "Current month commits",
      dataChartAcceptedClosed: "Accepted + Closed",
      dataChartClosed: "Closed",
      dataChartFound: "Found",
      dataChartLegendVulnerabilities: "Vulnerabilities",
      dataChartLegendWeek: "Weeks",
      days: "days",
      forces: {
        builds: "builds",
        indicators: {
          builds: {
            acceptedRisk: {
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
          hasForces: {
            protected: "Protected by Forces",
            protectedDesc: "Forces helps you build a safe system",
            title: "System status",
            unprotected: "Not protected by Forces",
            unprotectedDesc: "Vulnerable code may be deployed to production",
          },
          serviceUse: {
            title: "Service usage",
            total: "times",
          },
          strictness: {
            strict: "Strict",
            strictDesc: "Strict mode forces the fix of security issues",
            title: "Ratio of builds in Strict mode",
          },
        },
        subTitle: "Last 7 days",
        title: "Forces Analytics",
      },
      gitTitle: "Git Analytics",
      groupIsRemoving:
        "This group is expected to be removed on <strong>{{deletionDate}}</strong>" +
        "<br />Requested by <strong>{{userEmail}}</strong>",
      groupTitle: "Group Analytics",
      lastClosingVuln: {
        text: "Days since last closed vulnerability",
        tooltip: "Last time you fixed a vulnerability",
      },
      maxOpenSeverity: "Max open severity",
      maxSeverity: "Max severity found",
      meanRemediate: {
        text: "Mean time to remediate",
        tooltip:
          "Amount of time it will take your development team to fix a vulnerability",
      },
      open: "Open",
      pendingClosingCheck: {
        text: "Pending closing verification",
        tooltip:
          "Number of vulnerabilities you addressed and are pending for Fluid Attacks validation",
      },
      repositories: "Analyzed Repositories",
      statusGraph: "Status",
      success: "Group deletion was cancelled successfully",
      tags: {
        modalTitle: "Add tags information",
      },
      totalFindings: {
        text: "Total Findings",
        tooltip: "Number of types of vulnerabilities that you have",
      },
      totalVulnerabilitites: {
        text: "Total Vulnerabilities",
        tooltip:
          "Number of times that the total finding types repeat within your system",
      },
      treatmentAccepted: "Temporarily accepted",
      treatmentAcceptedUndefined: "Eternally accepted",
      treatmentGraph: "Treatment",
      treatmentInProgress: "In progress",
      treatmentNoDefined: "Not defined",
      undefinedTreatment: {
        text: "Open vulnerabilities with no defined treatment",
        tooltip:
          "Number of vulnerabilities that have a default treatment setting",
      },
    },
    tabObservations: {
      tabTitle: "Observations",
      tooltip:
        "Space to review the finding and suggest adjustments. For internal purposes only",
    },
    tabRecords: {
      editable: "Edit",
      editableTooltip: "Modify the records for this finding",
      tabTitle: "Records",
      tooltip:
        "Information that will be compromised or disclosed by exploiting the vulnerability",
    },
    tabResources: {
      addRepository: "Add",
      baseUrlPlaceholder: "gitlab.com/fluidattacks/product.git",
      branch: {
        label: "Branch",
        tooltip: "Target branch",
      },
      branchPlaceholder: "master",
      cannotRemove: "Cannot remove group, permission denied",
      changeState: "Change state",
      description: "Description",
      download: "Download",
      environment: {
        btnTooltip: "Add environments",
        text: "Environment",
      },
      environmentsTitle: "Environments",
      files: {
        btnTooltip: "Add a file",
        confirm: {
          title: "Remove File",
        },
        title: "Files",
      },
      groupToRemove:
        "Please type: <strong>{{projectName}}</strong>, to proceed",
      https: "HTTPS",
      invalidChars: "File name has invalid characters.",
      modalEnvTitle: "Add environment information",
      modalFileTitle: "Add file",
      modalOptionsContent: "What do you want to do with the file ",
      modalOptionsTitle: "File options",
      modalPlusBtn: {
        tooltip: "Add another repository",
      },
      modalRepoTitle: "Add repository information",
      modalTrashBtn: {
        tooltip: "Remove information about this repository",
      },
      noFileUpload: "Failed to upload the file",
      noSelection: "You must select an item from the table.",
      protocol: {
        label: "Protocol",
        tooltip: "Data transfer protocol",
      },
      removeGroup: "Delete Group",
      removeRepository: "Remove",
      repeatedInput: "There are repeated values in the form",
      repeatedItem: "One or more items to add exist already.",
      repository: {
        label: "Repository URL",
        tooltip: "Repository URL according to the protocol",
      },
      ssh: "SSH",
      success: "Item added successfully.",
      successChange: "Item state changed successfully.",
      successRemove: "Item removed successfully.",
      tags: {
        addTooltip: "Add a portfolio",
        removeTooltip: "Remove selected portfolio",
        title: "Portfolio",
      },
      totalEnvs: "Total environments: ",
      totalFiles: "Total files: ",
      uploadingProgress: "Uploading file...",
      warningMessage:
        "Deleting the group will remove its findings and related vulnerabilities." +
        "<br /> Deleted groups cannot be restored.",
    },
    tabSeverity: {
      attackComplexity: "Attack Complexity",
      attackComplexityOptions: {
        high: {
          text: "High",
          tooltip:
            "<strong>Bad:</strong> " +
            "A successful attack depends on conditions beyond the attacker's control. " +
            "That is, a successful attack cannot be accomplished at will, " +
            "but requires the attacker to invest in some measurable amount of effort in preparation or " +
            "execution against the vulnerable component before a successful attack can be expected.",
        },
        low: {
          text: "Low",
          tooltip:
            "<strong>Worst:</strong> " +
            "Specialized access conditions or extenuating circumstances do not exist. " +
            "An attacker can expect repeatable success when attacking the vulnerable component.",
        },
      },
      attackVector: "Attack Vector",
      attackVectorOptions: {
        adjacent: {
          text: "Adjacent network",
          tooltip:
            "<strong>Worse:</strong> " +
            "The vulnerable component is bound to the network stack, " +
            "but the attack is limited at the protocol level to a logically adjacent topology. " +
            "This can mean an attack must be launched from the same shared physical (e.g., Bluetooth or IEEE 802.11) " +
            "or logical (e.g., local IP subnet) network, or from within a secure or otherwise limited administrative domain " +
            "(e.g., MPLS, secure VPN to an administrative network zone). " +
            "One example of an Adjacent attack would be an ARP (IPv4) or neighbor discovery (IPv6) " +
            "flood leading to a denial of service on the local LAN segment.",
        },
        local: {
          text: "Local",
          tooltip:
            "<strong>Bad:</strong> " +
            "The vulnerable component is not bound to the network stack " +
            "and the attacker’s path is via read/write/execute capabilities. Either: " +
            "the attacker exploits the vulnerability by accessing the target system locally " +
            "(e.g., keyboard, console), or remotely (e.g., SSH); or " +
            "the attacker relies on User Interaction by another person to perform actions required " +
            "to exploit the vulnerability (e.g., using social engineering techniques to trick a legitimate user " +
            "into opening a malicious document).",
        },
        network: {
          text: "Network",
          tooltip:
            "<strong>Worst:</strong> " +
            "The vulnerable component is bound to the network stack and the set of possible attackers " +
            "extends beyond the other options listed below, up to and including the entire internet. " +
            'Such a vulnerability is often termed "remotely exploitable" and can be thought of as an attack being ' +
            "exploitable at the protocol level one or more network hops away (e.g., across one or more routers).",
        },
        physical: {
          text: "Physical",
          tooltip:
            "<strong>Bad:</strong> " +
            "The attack requires the attacker to physically touch or manipulate the vulnerable component. " +
            "Physical interaction may be brief (e.g., evil maid attack) or persistent. " +
            "An example of such an attack is a cold boot attack in which an attacker gains access " +
            "to disk encryption keys after physically accessing the target system. " +
            "Other examples include peripheral attacks via FireWire/USB Direct Memory Access (DMA).",
        },
      },
      authentication: "Authentication",
      authenticationOptions: {
        multipleAuth: "Multiple: Multiple authentication points",
        noAuth: "None: Authentication is not required",
        singleAuth: "Single: Single authentication point",
      },
      availability: "Availability Impact",
      availabilityImpact: "Availability Impact",
      availabilityImpactOptions: {
        high: {
          text: "High",
          tooltip:
            "<strong>Worst:</strong> " +
            "There is a total loss of availability, " +
            "resulting in the attacker being able to fully deny access to resources in the impacted component; " +
            "this loss is either sustained (while the attacker continues to deliver the attack) " +
            "or persistent (the condition persists even after the attack has completed). " +
            "Alternatively, the attacker has the ability to deny some availability, " +
            "but the loss of availability presents a direct, serious consequence to the impacted component " +
            "(e.g., the attacker cannot disrupt existing connections, but can prevent new connections; " +
            "the attacker can repeatedly exploit a vulnerability that, " +
            "in each instance of a successful attack, leaks a only small amount of memory, " +
            "but after repeated exploitation causes a service to become completely unavailable).",
        },
        low: {
          text: "Low",
          tooltip:
            "<strong>Bad:</strong> " +
            "Performance is reduced or there are interruptions in resource availability. " +
            "Even if repeated exploitation of the vulnerability is possible, " +
            "the attacker does not have the ability to completely deny service to legitimate users. " +
            "The resources in the impacted component are either partially available all of the time, " +
            "or fully available only some of the time, but overall there is no direct, " +
            "serious consequence to the impacted component.",
        },
        none: {
          text: "None",
          tooltip:
            "<strong>Good:</strong> " +
            "There is no impact to availability within the impacted component.",
        },
      },
      availabilityOptions: {
        complete: "Complete: There is a completely down target",
        none: "None: There is no impact",
        partial: "Partial: There is intermittency in the access to the target",
      },
      availabilityRequirement: "Availability Requirement",
      availabilityRequirementOptions: {
        high: {
          text: "High",
        },
        low: {
          text: "Low",
        },
        medium: {
          text: "Medium",
        },
      },
      complexity: "Access Complexity",
      complexityOptions: {
        highComplex:
          "High: Special conditions such as administrative access are required",
        lowComplex: "Low: No special conditions are required",
        mediumComplex:
          "Medium: Some conditions such as system access are required",
      },
      confidence: "Confidence Level",
      confidenceOptions: {
        confirmed:
          "Confirmed: The vulnerability is recognized by the manufacturer",
        notConfirm:
          "Not confirmed: There are few sources that recognize vulnerability",
        notCorrob:
          "Not corroborated: Vulnerability is recognized by unofficial sources",
      },
      confidentiality: "Confidentiality Impact",
      confidentialityImpact: "Confidentiality Impact",
      confidentialityImpactOptions: {
        high: {
          text: "High",
          tooltip:
            "<strong>Worst:</strong> " +
            "There is a total loss of confidentiality, " +
            "resulting in all resources within the impacted component being divulged to the attacker. " +
            "Alternatively, access to only some restricted information is obtained, " +
            "but the disclosed information presents a direct, serious impact. For example, " +
            "an attacker steals the administrator's password, or private encryption keys of a web server.",
        },
        low: {
          text: "Low",
          tooltip:
            "<strong>Bad:</strong> " +
            "There is some loss of confidentiality. Access to some restricted information is obtained, " +
            "but the attacker does not have control over what information is obtained, " +
            "or the amount or kind of loss is limited. " +
            "The information disclosure does not cause a direct, serious loss to the impacted component.",
        },
        none: {
          text: "None",
          tooltip:
            "<strong>Good:</strong> " +
            "There is no loss of confidentiality within the impacted component.",
        },
      },
      confidentialityOptions: {
        complete:
          "Complete: Total control over information related with the target",
        none: "None: There is no impact",
        partial: "Partial: Access to information but no control over it",
      },
      confidentialityRequirement: "Confidentiality Requirement",
      confidentialityRequirementOptions: {
        high: {
          text: "High",
        },
        low: {
          text: "Low",
        },
        medium: {
          text: "Medium",
        },
      },
      cvssVersion: "CVSS Version",
      editable: "Edit",
      editableTooltip: "Modify severity metrics",
      exploitability: "Exploitability",
      exploitabilityOptions: {
        conceptual: {
          text: "Conceptual: There are laboratory tests",
        },
        functional: {
          text: "Functional: There is an exploit",
          tooltip:
            "<strong>Worse:</strong> " +
            "Functional exploit code is available. " +
            "The code works in most situations where the vulnerability exists.",
        },
        high: {
          text: "High: Exploit is not required or it can be automated",
          tooltip:
            "<strong>Worst:</strong> " +
            "Functional autonomous code exists, " +
            "or no exploit is required (manual trigger) and details are widely available. " +
            "Exploit code works in every situation, " +
            "or is actively being delivered via an autonomous agent (such as a worm or virus). " +
            "Network-connected systems are likely to encounter scanning or exploitation attempts." +
            " Exploit development has reached the level of reliable, " +
            "widely available, easy-to-use automated tools.",
        },
        improbable: {
          text: "Improbable: There is no exploit",
        },
        proofOfConcept: {
          text: "Proof of Concept",
          tooltip:
            "<strong>Bad:</strong> " +
            "Proof-of-concept exploit code is available, " +
            "or an attack demonstration is not practical for most systems. " +
            "The code or technique is not functional in all situations and " +
            "may require substantial modification by a skilled attacker.",
        },
        unproven: {
          text: "Unproven",
          tooltip:
            "<strong>Good:</strong> " +
            "No exploit code is available, or an exploit is theoretical.",
        },
      },
      integrity: "Integrity Impact",
      integrityImpact: "Integrity Impact",
      integrityImpactOptions: {
        high: {
          text: "High",
          tooltip:
            "<strong>Worst:</strong> " +
            "There is a total loss of integrity, or a complete loss of protection. " +
            "For example, the attacker is able to modify any/all files protected by the impacted component. " +
            "Alternatively, only some files can be modified, but malicious modification would present a direct, " +
            "serious consequence to the impacted component.",
        },
        low: {
          text: "Low",
          tooltip:
            "<strong>Bad:</strong> " +
            "Modification of data is possible, " +
            "but the attacker does not have control over the consequence of a modification, " +
            "or the amount of modification is limited. The data modification does not have a direct, " +
            "serious impact on the impacted component.",
        },
        none: {
          text: "None",
          tooltip:
            "<strong>Good:</strong> " +
            "There is no loss of integrity within the impacted component.",
        },
      },
      integrityOptions: {
        complete: "Complete: Possibility to modify all target information",
        none: "None: There is no impact",
        partial: "Partial: Possibility to modify some target information",
      },
      integrityRequirement: "Integrity Requirement",
      integrityRequirementOptions: {
        high: {
          text: "High",
        },
        low: {
          text: "Low",
        },
        medium: {
          text: "Medium",
        },
      },
      modifiedAttackComplexity: "Modified Attack Complexity",
      modifiedAttackVector: "Modified Attack Vector",
      modifiedAvailabilityImpact: "Modified Availability Impact",
      modifiedConfidentialityImpact: "Modified Confidentiality Impact",
      modifiedIntegrityImpact: "Modified Integrity Impact",
      modifiedPrivilegesRequired: "Modified Privileges Required",
      modifiedSeverityScope: "Modified Scope",
      modifiedUserInteraction: "Modified User Interaction",
      privilegesRequired: "Privileges Required",
      privilegesRequiredOptions: {
        high: {
          text: "High",
          tooltip:
            "<strong>Bad:</strong> " +
            "The attacker requires privileges that provide significant (e.g., administrative) control " +
            "over the vulnerable component allowing access to component-wide settings and files.",
        },
        low: {
          text: "Low",
          tooltip:
            "<strong>Worse:</strong> " +
            "The attacker requires privileges that provide basic user capabilities " +
            "that could normally affect only settings and files owned by a user. " +
            "Alternatively, an attacker with Low privileges has the ability to access only non-sensitive resources.",
        },
        none: {
          text: "None",
          tooltip:
            "<strong>Worst:</strong> " +
            "The attacker is unauthorized prior to attack, and therefore does not require any access to settings " +
            "or files of the vulnerable system to carry out an attack.",
        },
      },
      remediationLevel: "Remediation Level",
      remediationLevelOptions: {
        officialFix: {
          text: "Official Fix",
          tooltip:
            "<strong>Good:</strong> " +
            "A complete vendor solution is available. " +
            "Either the vendor has issued an official patch, or an upgrade is available.",
        },
        temporaryFix: {
          text: "Temporary Fix",
          tooltip:
            "<strong>Bad:</strong> " +
            "There is an official but temporary fix available. " +
            "This includes instances where the vendor issues a temporary hotfix, tool, or workaround.",
        },
        unavailable: {
          text: "Unavailable",
          tooltip:
            "<strong>Worst:</strong> " +
            "There is either no solution available or it is impossible to apply.",
        },
        workaround: {
          text: "Workaround",
          tooltip:
            "<strong>Bad:</strong> " +
            "There is an unofficial, non-vendor solution available. " +
            "In some cases, users of the affected technology will create a patch of their own or " +
            "provide steps to work around or otherwise mitigate the vulnerability.",
        },
      },
      reportConfidence: "Report Confidence",
      reportConfidenceOptions: {
        confirmed: {
          text: "Confirmed",
          tooltip:
            "<strong>Worst:</strong> " +
            "Detailed reports exist, " +
            "or functional reproduction is possible (functional exploits may provide this). " +
            "Source code is available to independently verify the assertions of the research, " +
            "or the author or vendor of the affected code has confirmed the presence of the vulnerability.",
        },
        reasonable: {
          text: "Reasonable",
          tooltip:
            "<strong>Bad:</strong> " +
            "Significant details are published, " +
            "but researchers either do not have full confidence in the root cause, or " +
            "do not have access to source code to fully confirm all of the interactions that may lead to the result. " +
            "Reasonable confidence exists, however, that the bug is reproducible and " +
            "at least one impact is able to be verified (proof-of-concept exploits may provide this). " +
            "An example is a detailed write-up of research into a vulnerability with an explanation " +
            '(possibly obfuscated or "left as an exercise to the reader") ' +
            "that gives assurances on how to reproduce the results.",
        },
        unknown: {
          text: "Unknown",
          tooltip:
            "<strong>Bad:</strong> " +
            "There are reports of impacts that indicate a vulnerability is present. " +
            "The reports indicate that the cause of the vulnerability is unknown, " +
            "or reports may differ on the cause or impacts of the vulnerability. " +
            "Reporters are uncertain of the true nature of the vulnerability, " +
            "and there is little confidence in the validity of the reports or " +
            "whether a static Base Score can be applied given the differences described. " +
            "An example is a bug report which notes that an intermittent but non-reproducible crash occurs, " +
            "with evidence of memory corruption suggesting that denial of service, " +
            "or possible more serious impacts, may result.",
        },
      },
      resolution: "Resolution Level",
      resolutionOptions: {
        nonExistent: "Non-existent: There is no solution",
        official: "Official: There is a manufacturer available patch",
        palliative:
          "Palliative: There is a patch that was not published by the manufacturer",
        temporal: "Temporal: There are temporary solutions",
      },
      severityScope: "Scope",
      severityScopeOptions: {
        changed: {
          text: "Changed",
          tooltip:
            "<strong>Worst:</strong> " +
            "An exploited vulnerability can affect resources beyond the security scope" +
            " managed by the security authority of the vulnerable component. " +
            "In this case, the vulnerable component and the impacted component are different " +
            "and managed by different security authorities.",
        },
        unchanged: {
          text: "Unchanged",
          tooltip:
            "<strong>Bad:</strong> " +
            "An exploited vulnerability can only affect resources managed by the same security authority. " +
            "In this case, the vulnerable component and the impacted component are either the same, " +
            "or both are managed by the same security authority.",
        },
      },
      solve: "Mark as solved",
      tabTitle: "Severity",
      tooltip: "Assigned score according to CVSS 3.1 metrics",
      update: "Update",
      userInteraction: "User Interaction",
      userInteractionOptions: {
        none: {
          text: "None",
          tooltip:
            "<strong>Worst:</strong> The vulnerable system can be exploited without interaction from any user.",
        },
        required: {
          text: "Required",
          tooltip:
            "<strong>Bad:</strong> Successful exploitation of this vulnerability requires a user to take some " +
            "action before the vulnerability can be exploited. For example, a successful exploit may only be possible" +
            " during the installation of an application by a system administrator.",
        },
      },
      vector: "Access Vector",
      vectorOptions: {
        adjacent: "Adjacent network: Exploitable from same network segment",
        local: "Local: Exploitable with local access to the target",
        network: "Network: Exploitable from Internet",
      },
    },
    tabTracking: {
      accepted: "Temporally accepted",
      acceptedUndefined: "Eternally accepted",
      closed: "Closed",
      cycle: "Cycle",
      effectiveness: "Effectiveness",
      found: "Found",
      inProgress: "In progress",
      justification: "Justification:",
      manager: "Manager:",
      new: "New",
      open: "Open",
      pending: "Pending",
      status: "Status",
      tabTitle: "Tracking",
      tooltip:
        "Evolution of the finding over time: historical records, open/closed vulnerabilities, " +
        "and temporally/eternally accepted treatments",
      treatment: "Treatment",
      vulnerabilitiesAcceptedTreatment:
        "{{count}} vulnerabilities were accepted temporally",
      vulnerabilitiesAcceptedUndefinedTreatment:
        "{{count}} vulnerabilities were accepted eternally",
      vulnerabilitiesClosed: "Vulnerabilities closed:",
      vulnerabilitiesFound: "Vulnerabilities found:",
    },
    tabUsers: {
      addButton: {
        text: "Add",
        tooltip: "Add a user to this group",
      },
      daysAgo: "{{count}} day ago",
      daysAgoPlural: "{{count}} days ago",
      editButton: {
        text: "Edit",
        tooltip: "Select a user and edit their information",
      },
      editStakeholderTitle: "Edit stakeholder information",
      hoursAgo: "{{count}} hour ago",
      hoursAgoPlural: "{{count}} hours ago",
      minutesAgo: "{{count}} minute ago",
      minutesAgoPlural: "{{count}} minutes ago",
      monthsAgo: "{{count}} month ago",
      monthsAgoPlural: "{{count}} months ago",
      noSelection: "You must select an email from the table.",
      removeUserButton: {
        text: "Remove",
        tooltip: "Remove a user from the group, first select one",
      },
      success: ", an email will be sent to confirm the registration.",
      successAdmin: "Stakeholder information updated.",
      successDelete: " was removed from this group.",
      textbox:
        "Enter the email of the person you wish to add, it must be " +
        "an Office 365 or Google email",
      title: "Add stakeholder to this group",
      titleSuccess: "Congratulations",
    },
    tabVuln: {
      alerts: {
        acceptationNotRequested: "Indefinite acceptation is not requested",
        acceptationSuccess: "Indefinite acceptation has been handled",
        hasNewVulns:
          "The treatment is set as new, please select a treatment for the vulnerability.",
        hasNewVulnsPlural:
          "The treatment on one or more vulnerabilities is set as new, please select a treatment for the vulnerabilities.",
        maximumNumberOfAcceptations:
          "Vulnerability has been accepted the maximum number of times allowed by the organization",
        treatmentChange: "Vulnerability treatment will be changed",
        uploadFile: {
          invalidRoot:
            "Active root not found for the repo. Verify the nickname in the scope tab",
          invalidStream: "Invalid stream, it must start with 'home'",
          key: "Key '{{key}}' is missing or invalid. ",
          value: "Value is invalid, pattern '{{pattern}}'. ",
        },
      },
      buttons: {
        edit: "Bulk edit",
        handleAcceptation: "Treatment Acceptation",
        reattack: "Reattack",
      },
      buttonsTooltip: {
        cancel: "Cancel",
        edit: "Modify the fields of the vulnerabilities",
        handleAcceptation: "Approve/Reject treatment",
      },
      close: "Close",
      closed: "Closed",
      commitHash: "Commit hash",
      contentTab: {
        details: {
          title: "Details",
          tooltip: "Details",
        },
        treatments: {
          title: "Treatments",
          tooltip: "Modify the treatment of the vulnerability",
        },
      },
      exceptions: {
        sameValues: "Same values",
        severityOutOfRange:
          "Vulnerability cannot be accepted, severity outside of range set by the organization",
      },
      info: {
        text: "Please select vulnerabilities to reattack",
        title: "Info",
      },
      notApplicable: "n/a",
      open: "Open",
      requested: "Requested",
      searchText: "Search Text",
      status: "Status",
      statusTooltip:
        "Filter vulnerabilities based on their open / closed status",
      tabTitle: "Locations",
      tooltip: "Open / Closed vulnerabilities",
      verified: "Verified",
      vulnTable: {
        currentTreatment: "Current",
        cycles: "Cycles",
        efficacy: "Efficiency",
        info: "Info",
        lastReattackDate: "Last reattack date",
        lastRequestedReattackDate: "Last request date",
        location: "Location",
        more: "...",
        reattack: "Reattack: ",
        reattacks: "Reattacks",
        reattacksTooltip:
          "Filter vulnerabilities based on the status of their reattack requests",
        reportDate: "Report date",
        requester: "Requester",
        specific: "Specific",
        status: "Status: ",
        treatmentChanges: "Changes",
        treatmentDate: "Date",
        treatmentExpiration: "Expiration",
        treatmentJustification: "Justification",
        treatmentManager: "Manager",
        treatments: "Treatments",
        treatmentsTooltip:
          "Filter vulnerabilities based on the treatment they were given",
        verification: "Last reattack",
        vulnType: {
          inputs: "app",
          lines: "code",
          ports: "infra",
          title: "Type",
        },
        where: "Where",
      },
      vulnerabilityInfo: "Vulnerability",
    },
    usersTable: {
      firstlogin: "First login",
      invitation: "Invitation",
      lastlogin: "Last login",
      phoneNumber: "Phone Number",
      userOrganization: "Organization",
      userResponsibility: "Responsibility",
      userRole: "Role",
      usermail: "Stakeholder email",
    },
  },
  sidebar: {
    commit: "Commit:",
    configuration: {
      text: "Config",
      tooltip: "Some additional configurations here",
    },
    deploymentDate: "Deploy date:",
    newOrganization: {
      modal: {
        invalidName: "Name specified for the organization is not allowed",
        name: "Organization Name",
        nameTooltip:
          "Random name that will be assigned to your new organization",
        namesUnavailable:
          "There are no available organization names at the moment",
        success: "Organization {{name}} created successfully",
        successTitle: "Success",
        title: "Add new organization",
      },
      text: "Add Organization",
      tooltip: "Create new organization",
    },
    reports: "Reports",
    user: {
      text: "Add Stakeholder",
      tooltip: "Add a user",
    },
  },
  tagIndicator: {
    acceptedVulnerabilitiesBySeverity: "Accepted vulnerabilities by severity",
    acceptedVulnerabilitiesByUser: "Accepted vulnerabilities by user",
    criticalSeverity: "Critical Severity",
    findingsGroup: "Findings by group",
    highSeverity: "High Severity",
    lowSeverity: "Low Severity",
    meanRemediate: "Mean (average) days to remediate",
    mediumSeverity: "Medium Severity",
    openFindingsGroup: "Open findings by group",
    openVuln: "open vulns.",
    openVulnsGroups: "Open vulnerabilities by group",
    remediatedAcceptedVuln:
      "How many vulnerabilities are remediated and accepted?",
    remediatedVuln: "How many vulnerabilities are remediated (closed)?",
    topFindingsByVulnerabilities: "Top findings (by open vulnerabilities)",
    topOldestFindings: "Top oldest findings",
    totalVuln: "vulnerabilities",
    undefinedTitle: "Treatmentless by group",
    undefinedVuln: "undefined",
    vulnerabilitiesByLevel: "Vulnerabilities by level",
    vulnerabilitiesByTag: "Vulnerabilities by tag",
    vulnerabilitiesByTreatments: "Vulnerabilities by treatments",
    vulnerabilitiesByType: "Vulnerabilities by type",
    vulnsGroups: "Vulnerabilities by group",
  },
  updateAccessToken: {
    accessToken: "Personal Access Token",
    close: "Close",
    copy: {
      copy: "Copy",
      failed: "It cannot be copied",
      success: "Token copied",
      successfully: "Token copied successfully",
    },
    delete: "Token invalidated successfully",
    expirationTime: "Expiration date",
    invalidExpTime:
      "Expiration time must be minor than six month and greater than current date",
    invalidate: "Revoke current token",
    invalidated: "Invalidated token",
    message:
      "Please save this access token in a safe location. You will not be able to see it again after closing " +
      "this dialog.",
    success: "Updated access token",
    successfully: "Token updated successfully",
    title: "Update access token",
    tokenCreated: "Token created at: ",
  },
  updateForcesToken: {
    accessToken: "DevSecOps token",
    close: "Close",
    copy: {
      copy: "Copy",
      failed: "It cannot be copied",
      success: "DevSecOps Token copied",
      successfully: "DevSecOps Token copied successfully",
    },
    generate: "Generate",
    reset: "Reset",
    revealToken: "Reveal Token",
    success: "Updated DevSecOps token",
    successfully: "DevSecOps token updated successfully",
    title: "Manage DevSecOps token",
    tokenNoExists: "A token could not be found for the group",
  },
  userModal: {
    emailPlaceholder: "someone@domain.com",
    emailText:
      "Enter the email of the person you wish to add, it must be " +
      "an Office 365 or Google email",
    organization: "Organization",
    phoneNumber: "Phone Number",
    responsibility: "Responsibility",
    responsibilityPlaceholder: "Product Owner, Group Manager, Tester, ...",
    role: "Role",
    roles: {
      admin: "Admin",
      analyst: "Analyst",
      closer: "Closer",
      customer: "User",
      customeradmin: "User Manager",
      executive: "Executive",
      groupManager: "Group Manager",
      resourcer: "Resourcer",
      reviewer: "Reviewer",
    },
    success: "{{email}} was added successfully",
  },
  validations: {
    alphanumeric: "Only alphanumeric characters",
    between: "This value must be between {{min}} and {{max}}",
    columns: "At least 1 column must be shown",
    datetime: "The datetime format is not valid",
    draftTitle: "The title format is not valid",
    email: "The email format is not valid",
    excludeFormat: "Root name should not be included in the exception pattern",
    fileSize: "The file size must be less than {{count}}MB",
    fluidAttacksStaffWithoutFluidAttacksService:
      "Groups without an active Fluid Attacks service " +
      "can not have Fluid Attacks staff",
    greaterDate: "The date must be today or before",
    infectedFile: "Our system detected that the uploaded file is infected",
    invalidChar:
      "Invalid characters, use: alphanumerics, spaces and punctuations",
    invalidCommentParent: "The comment parent is invalid",
    invalidEmailInField: "The email address inserted is not valid",
    invalidFieldLength: "The value inserted in one of the fields is too large",
    invalidPhoneNumberInField: "The phone number inserted is not valid",
    invalidTextBeginning:
      "Field cannot begin with the following character: {{ chars }}",
    invalidTextField:
      "Field cannot contain the following characters: {{chars}}",
    invalidUrlField:
      "URL value cannot contain the following characters: {{chars}}",
    invalidValueInField: "The value inserted in one of the fields is not valid",
    lowerDate: "Invalid date",
    maxLength: "This field requires less than {{count}} characters",
    minLength: "This field requires at least {{count}} characters",
    noFluidAttacksHackersInFluidAttacksService:
      "Groups with any active Fluid Attacks service " +
      "can only have Hackers provided by Fluid Attacks",
    numeric: "This field can only contain numbers",
    requireNickname: "Nickname already exist",
    required: "Required field",
    someRequired: "Select at least one value",
    stakeholderHasGroupAccess:
      "The stakeholder has been granted access to the group previously",
    tags: "This field can only contain alphanumeric characters and dashes",
    validDate: "The date must be below six months",
    validDateToken: "The date must be below six months",
    validSessionDate: "The session has expired",
  },
};

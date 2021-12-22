import type { ResourceKey } from "i18next";

export const enTranslations: ResourceKey = {
  analytics: {
    barChart: {
      exposureByGroups: "Open Severity by groups",
      meanTimeToRemediate: {
        tooltip: {
          alt: {
            default: "Mean time to remediate",
            nonTreated: "Non treated mean time to remediate",
            nonTreatedCvssf: "Non treated mean time to remediate & severity",
          },
          default: "Mean time to remediate & severity",
        },
      },
      mttrBenchmarking: {
        title: "MTTR Benchmarking",
        tooltip: {
          all: "Days per Severity for all vulnerabilities",
          nonTreated: "Days per Severity for non treated vulnerabilities",
        },
      },
      topVulnerabilities: {
        altTitle: {
          app: "App Open Severity (CVSSF)",
          code: "Code Open Severity (CVSSF)",
          infra: "Infra Open Severity (CVSSF)",
          vulnerabilities: "Top vulnerabilities",
        },
        title: "Open Severity by type",
        tooltip: {
          app: "Source of severity of type App",
          code: "Source of severity of type Code",
          cvssf: "Severity",
          infra: "Source of severity of type Infra",
          vulnerabilities: "Vulnerabilities",
        },
      },
    },
    disjointForceDirectedGraph: {
      whereToFindings: {
        title: "Systems Risk",
      },
    },
    emptyChart: {
      text: "Your data will be available soon!",
    },
    gauge: {
      forcesBuildsRisk: {
        title: "Builds risk",
      },
      forcesSecurityCommitment: {
        footer: {
          acceptedRisk:
            "However, accepted vulnerabilities on ASM are ignored by the strict mode, " +
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
        title: "Active resources distribution",
      },
      treatment: {
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
      cvssfBenchmarking: {
        title: "Remediation Rate Benchmarking",
      },
      distributionOverTimeCvssf: {
        title: "Distribution over time",
        tooltip: {
          cvssf: "Severity",
          vulnerabilities: "Vulnerabilities",
        },
      },
      exposedOverTimeCvssf: {
        title: "Total Exposure",
      },
      riskOverTime: {
        altTitle: "Vulnerabilities over time",
        title: "Severity over time",
        tooltip: {
          cvssf: "Severity",
          vulnerabilities: "Vulnerabilities",
        },
      },
    },
    textBox: {
      daysSinceLastRemediation: {
        title: "Days since last remediation",
      },
      findingsBeingReattacked: {
        title: "Vulnerabilities being re-attacked",
      },
      forcesAutomatizedVulns: {
        title: "Automatized Vulnerabilities",
      },
      forcesRepositoriesAndBranches: {
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
        title: "Service usage",
      },
      totalTypes: {
        title: "Total types",
      },
      totalVulnerabilities: {
        title: "Total vulnerabilities",
      },
      vulnsWithUndefinedTreatment: {
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
    comments: {
      label: "Consulting notifications:",
      subscribed: "Yes",
      tooltip:
        "Receive notifications by email for comments posted on your subscribed groups",
      unsubscribed: "No",
    },
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
    allOptions: "--All options--",
    clearFilters: "Clear Filters",
    filterRes1: "Filtered",
    filterRes2: "of",
    filters: "Filters",
    more: "--View More--",
    noDataIndication: "There is no data to display",
    search: "Search",
    tooltip: "Search filters for the table",
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
      filtersTooltips: {
        actor: "Filter by author",
        groupsContributed: "Filter by groups contributed",
        repository: "Filter by repository",
      },
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
      hint: {
        description: "Hint: Description",
        empty: "Not available",
      },
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
      filtersTooltips: {
        accessibility: "Filter by accessibility",
        actAfterBlock: "Filter by action after blocking",
        actBefBlock: "Filter by action before blocking",
        affectedComponents: "Filter by affected components",
        closingDate: "Filter by closing date",
        date: "Filter by date",
        status: "Filter by status",
        type: "Filter by type",
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
          toeUnaccessible: "ToE inaccessibility",
          toeUnavailable: "ToE unavailability",
          toeUnstability: "ToE instability",
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
        root: "Root",
        rootPlaceholder: "Search by nickname...",
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
        reattack: "Pending reattack:",
        title: "Description",
        value: "{{count}} day ago",
        // eslint-disable-next-line camelcase -- It is required for react-i18next
        value_plural: "{{count}} days ago",
      },
      evidence: {
        edit: "Edit",
        noData: "There are no evidences",
      },
      exportCsv: {
        text: "Export",
        tooltip: "Export to a comma-separated values file",
      },
      filtersTooltips: {
        age: "Filter by age",
        lastReport: "Filter by last report",
        reattack: "Filter by reattack",
        releaseDate: "filter by Release Date",
        severity: "Filter by severity",
        status: "Filter by status",
        tags: "Filter by Tags",
        treatment: "Filter by Treatment",
        type: "Filter by type",
        where: "Filter by text on 'Where' column",
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
        noMobileAppWarning:
          "Reports are created on-demand and are protected by a <strong>passphrase</strong>. " +
          "The <strong>passphrase</strong> is generated randomly and will be " +
          "sent through a notification to your mobile device. In order to receive it, " +
          "you will need to download and set up the ASM mobile app, please " +
          "download it and try again.",
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
      filtersTooltips: {
        date: "Filter by date",
        kind: "Filter by type",
        repository: "Filter by repository",
        status: "Filter by status",
        strictness: "Filter by strictness",
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
          tooltip:
            "Log record of the DevSecOps execution in rich console format",
        },
        summary: {
          text: "Summary",
          tooltip: "Status summary of found vulnerabilities",
        },
      },
    },
    machine: {
      date: {
        create: "Queue date",
        duration: "Duration",
        start: "Start time",
        stop: "Finish date",
      },
      executionDetailsModal: {
        title: "Execution details",
      },
      finding: {
        finding: "Finding",
        modified: "Modified",
        open: "Open",
      },
      job: {
        id: "Batch job id",
        name: "Job name",
        queue: "Batch queue name",
      },
      root: "Root",
      rootId: "Root Id",
      tableAdvice: "Click on an execution to see more details",
    },
    scope: {
      common: {
        add: "Add new root",
        addTooltip: "Add a new git root to this group",
        changeWarning:
          "This is a change in the scope of the test service, which may involve closing or reporting new vulnerabilities.",
        confirm: "Confirm change",
        deactivation: {
          closedDastVulnsWarning:
            " DAST vulnerabilities will be closed deactivating this root.",
          closedSastVulnsWarning:
            " SAST vulnerabilities will be closed deactivating this root.",
          confirm:
            "Deactivating this root takes it out of scope, therefore it will no longer be tested.",
          errors: {
            changed:
              "This root was just updated, please review the changes and try again",
          },
          loading: "...",
          reason: {
            label: "Reason",
            mistake: "Registered by mistake",
            moved: "Moved to another group",
            scope: "Out of scope",
          },
          success: {
            message:
              "You will be notified via email once the process is complete",
            title: "Success",
          },
          targetGroup: "Target group",
          targetPlaceholder: "Search by group name...",
          title: "Deactivate Root",
          warning:
            "Adding this root to the scope again will count it as new. No history or other associated data will be kept.",
        },
        edit: "Edit root",
        editTooltip: "Edit the selected git root",
        errors: {
          duplicateNickname:
            "An active root with the same Nickname already exists " +
            "please type a new nickname",
          duplicateUrl:
            "An active root with the same URL already exists " +
            "within the organization",
          hasVulns:
            "Can't update as there are already vulnerabilities reported for this root",
        },
        lastCloningStatusUpdate: "Last status update",
        lastStateStatusUpdate: "Last state update",
        state: "State",
      },
      git: {
        confirmBranch: "Make sure the new branch is equivalent to the old one",
        envUrls: "Environment URLs",
        errors: {
          invalid: "Repository URL or branch are not valid",
          rootInGitignore:
            "Root name should not be included in gitignore pattern",
        },
        filter: {
          exclude: "Exclusions",
          placeholder: "**/example.txt",
          title: "Filters",
          tooltip:
            "Patterns that define which files should be ignored during the analysis",
          warning:
            "Vulnerabilities of various impact can exist in test directories. " +
            "We recommend you do not exclude any part of your repository. " +
            "Decide at your own risk.",
        },
        filtersTooltips: {
          branch: "Filter by branch",
          nickname: "Filter by nickname",
          state: "Filter by state",
          status: "Filter by status",
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
        nickname: "Nickname",
        port: "Port",
        title: "IP Roots",
      },
      url: {
        errors: {
          invalid: "Invalid URL",
        },
        host: "Host",
        nickname: "Nickname",
        path: "Path",
        port: "Port",
        protocol: "Protocol",
        title: "URL Roots",
        url: "URL",
      },
    },
    stakeHolders: {
      filtersTooltips: {
        invitation: "Filter by invitation",
        role: "Filter by role",
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
        text: "Surface",
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
        root: "Root",
        seenFirstTimeBy: "Seen first time by",
        testedDate: "Attacked at",
      },
      lines: {
        actionButtons: {
          editButton: {
            success: "was successfully edited",
            text: "Edit",
            tooltip: "Edit attacked lines",
          },
        },
        attackedAt: "Attacked at",
        attackedBy: "Attacked by",
        attackedLines: "Attacked lines",
        bePresent: "Be present",
        bePresentUntil: "Be present until",
        comments: "Comments",
        commitAuthor: "Commit author",
        coverage: "Coverage",
        daysToAttack: "Days to attack",
        editModal: {
          alerts: {
            alreadyUpdate: "Something modified the lines during the edition.",
            invalidAttackedAt:
              "The attacked at is not valid. There is a new datetime.",
            invalidAttackedLines:
              "The attacked lines are not valid. Loc has been changed.",
            nonPresent: "The lines is not present.",
            success: "Lines has been updated.",
          },
          close: "Close",
          fields: {
            attackedAt: "Attacked at",
            attackedLines: "Attacked lines",
            attackedLinesComment: "LOC is set by default",
            comments: "What comments do you have?",
          },
          procced: "Proceed",
          title: "Edit attacked lines",
        },
        filename: "Filename",
        firstAttackAt: "First attack at",
        loc: "LOC",
        modifiedCommit: "Modified commit",
        modifiedDate: "Modified date",
        no: "No",
        root: "Root",
        seenAt: "Seen at",
        sortsRiskLevel: "Priority (IA/ML)",
        yes: "Yes",
      },
      tabs: {
        inputs: {
          text: "Inputs",
          tooltip:
            "Track which application/infrastructure inputs have been reviewed",
        },
        lines: {
          text: "Lines",
          tooltip: "Track which source code lines have been reviewed",
        },
      },
    },
  },
  groupAlerts: {
    acceptanceApproved: "Indefinite acceptance has been approved",
    acceptanceRejected: "Indefinite acceptance has been rejected",
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
    expectedPathToStartWithRepo:
      "Expected path to start with the repo nickname",
    expectedVulnToHaveNickname: "Expected vulnerability to have repo_nickname",
    expiredInvitation: "The stakeholder has an expired invitation",
    fileTypeCsv: "The file must have .csv extension",
    fileTypeEvidence: "The image must be .png or .gif type",
    fileTypePy: "The file must have .py or .exp extension",
    fileTypeWrong: "The file has an unknown or non-allowed format",
    fileTypeYaml: "The file must be .yaml or .yml type",
    fileUpdated: "File updated ;)",
    groupInfoUpdated: "Group information updated successfully",
    invalid: "is invalid",
    invalidAssigned: "Please select a valid assigned user",
    invalidCannotModifyNicknameWhenClosing:
      "Invalid, you cannot change the nickname while closing",
    invalidDate:
      "The date must be minor than six month and greater than current date",
    invalidNOfVulns: "You can upload a maximum of 100 vulnerabilities per file",
    invalidSchema: "The uploaded file does not match the schema",
    invalidSpecific: "Invalid field/line/port",
    invalidStructure: "The provided file has a wrong structure",
    key: "Key",
    noFileSelected: "No file selected",
    noFileUpdate: "Failed to update the file",
    noFound: "Vulnerabilities in the request not found",
    noVerificationRequested: "No verification requested",
    onlyNewVulnerabilitiesOpenState:
      "Only new vulnerabilities with Open state are allowed",
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
    requestedReattackSuccess: "A reattack has been requested successfully",
    requestedZeroRiskSuccess: "Zero risk vulnerability has been requested",
    titleSuccess: "Congratulations",
    updated: "Updated",
    updatedTitle: "Correct!",
    value: "Value",
    verificationAlreadyRequested: "Verification already requested",
    verifiedSuccess: "The vulnerability was marked as verified",
    verifiedSuccessPlural: "The vulnerabilities were marked as verified",
    vulnClosed: "Vulnerability has already been closed",
    zeroRiskAlreadyRequested: "Zero risk vulnerability already requested",
    zeroRiskIsNotRequested: "Zero risk vulnerability is not requested",
  },
  info: {
    commit: "Commit:",
    deploymentDate: "Deploy date:",
  },
  legalNotice: {
    acceptBtn: {
      text: "Accept and continue",
      tooltip: "Click if you understand and accept the terms above",
    },
    description: {
      legal:
        "ASM, Copyright (c) {{currentYear}} Fluid Attacks. This platform contains " +
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
      privacy:
        "By using the Fluid Attacks' Attack Surface Manager, you agree to our ",
      privacyLinkText: "Privacy Policy",
    },
    rememberCbo: {
      text: "Remember my decision",
      tooltip: "Mark the checkbox if you want this decision to be permanent",
    },
    title: "Legal notice",
  },
  login: {
    auth: "Welcome back, please authenticate to proceed.",
    bitbucket: "Sign in with Bitbucket",
    google: "Sign in with Google",
    microsoft: "Sign in with Microsoft",
    newuser: "If you are a new user, click below to sign up.",
  },
  navbar: {
    config: {
      text: "Configuration",
      tooltip: "Some additional configurations here",
    },
    deleteAccount: {
      modal: {
        text:
          "This action will immediately delete the account from ASM. " +
          "This is a destructive action.",
        warning: "Warning!",
      },
      text: "Delete Account",
      tooltip: "Delete account from ASM",
    },
    help: {
      chat: "Live Chat",
      expert: "Talk to an expert",
    },
    logout: {
      text: "Log out",
      tooltip: "Log out of ASM",
    },
    newsTooltip: "Latest updates about ASM",
    role: "Role:",
    searchPlaceholder: "Search Group Name",
    token: {
      text: "API",
      tooltip: "Get an ASM API Token",
    },
    uploadFile: {
      text: "Upload a file",
      tooltip: "Upload a file to evaluate",
    },
    user: {
      text: "Add Stakeholder",
      tooltip: "Add a user",
    },
  },
  organization: {
    tabs: {
      analytics: {
        text: "Analytics",
        tooltip: "Organization status at a glance",
      },
      billing: {
        text: "Billing",
        tooltip: "Billing and subcriptions for your organization",
      },
      groups: {
        disabled: "Disabled",
        enabled: "Enabled",
        filtersTooltips: {
          groupName: "Filter by group name",
          machine: "Filter by machine",
          service: "Filter by service",
          squad: "Filter by squad",
          subscription: "Filter by subscription",
        },
        newGroup: {
          description: {
            text: "Description",
            tooltip: "Brief description to identify the group",
          },
          extraChargesMayApply: "Extra charges may apply",
          language: {
            EN: "English",
            ES: "Spanish",
            text: "Report Language",
            tooltip: "Language in which findings should be reported",
          },
          machine: {
            text: "Include Machine service?",
            tooltip:
              "Vulnerability detection tool that scans and reports security issues in your source code",
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
          service: {
            black: "Black",
            title: "Service type",
            white: "White",
          },
          squad: {
            text: "Include Squad Service?",
            tooltip:
              "Squad finds deep and zero-day vulnerabilities during software development",
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
            "Acceptance severity score must be a positive floating number between 0.0 and 10.0",
          acceptanceSeverityRange:
            "Minimum acceptance score should be lower than the maximum value",
          invalidBreakableSeverity:
            "The minimum breaking severity score must be a positive floating number between 0.0 and 10.0",
          maxAcceptanceDays:
            "Maximum acceptance days should be a positive integer between 0 and 180",
          maxNumberAcceptances:
            "Maximum number of acceptances should be a positive integer",
        },
        findings: {
          addPolicies: {
            success:
              "Remember that the application of the policy requires the approval of a user with manager role",
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
          form: {
            finding: "Finding",
            tags: "Tags",
          },
          handlePolicies: {
            success: {
              approved: "The policy will be applied within the next minutes",
              rejected: "The policy was successfully rejected",
            },
          },
          submitPolicies: {
            modalTitle: "Re-submit organization finding policy",
          },
          title: "Organization Findings Policies",
          tooltip: {
            addButton: "Add organization policy pending to approve",
            approveButton: "Approve organization finding policy",
            deactivateButton: "Disable organization finding policy",
            nameInput:
              "Add the type of finding to which vulnerabilities in organization " +
              "groups will apply the accepted permanently treatment",
            rejectButton: "Reject organization finding policy",
            resubmitButton: "Re-submit organization finding policy",
            tagsInput: "Tags associated to the policy",
          },
        },
        permissionTooltip:
          "You need to have a User Manager role to be able to modify " +
          "these values",
        policies: {
          acceptanceSeverityRange:
            "Temporal CVSS 3.1 score range between which a finding can be accepted",
          maxAcceptanceDays:
            "Maximum number of calendar days a finding can be temporarily accepted",
          maxNumberAcceptances:
            "Maximum number of times a finding can be temporarily accepted",
          minBreakingSeverity:
            "Minimum CVSS 3.1 score of an open vulnerability for DevSecOps to" +
            " break the build in strict mode",
        },
        policy: "Policy",
        recommended: {
          acceptanceDays: "0",
          acceptanceSeverity: "0.0    -    0.0",
          breakableSeverity: "0.0",
          numberAcceptances: "0",
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
    acceptanceButtons: {
      approve: "Approve Acceptance",
      reject: "Reject Acceptance",
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
    findingDeleted: "Finding was deleted",
    findingRejected: "Finding {{findingId}} was rejected",
    findingsDeleted: "Findings were deleted",
    groupAccessInfoSection: {
      disambiguation: "Disambiguation",
      groupContext: "Group context",
      markdownAlert:
        "Please use Markdown language for writing this information.",
      noDisambiguation:
        "There is no need for disambiguation in this group at the moment.",
      noGroupContext:
        "There is no information on how to access this group's ToE at the moment.",
      tooltips: {
        editDisambiguationInfo: "Edit group disambiguation",
        editGroupContext: "Edit group context information",
      },
    },
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
      asm: "ASM",
      black: "Black",
      continuous: "Continuous Hacking",
      deleteGroup: {
        deleteGroup: "Delete this group",
        reason: {
          diffSectst: "Different security testing strategy",
          migration: "Information will be moved to a different group",
          noSectst: "No more security testing",
          noSystem: "System will be deprecated",
          other: "Other reason not mentioned here",
          title: "Please select the reason why you want to delete this group.",
          tooltip: "Reason of group deletion",
        },
        typeGroupName: "Please type the group name to proceed.",
        warning: "Group deletion is a destructive action and cannot be undone.",
        warningBody:
          "This action will immediately delete the group. " +
          "This will remove all of its data including findings and related vulnerabilities. " +
          "This is a destructive action and cannot be undone.",
        warningTitle: "Warning!",
      },
      deletedsoon: "Scheduled to be deleted in 1 month",
      errors: {
        activeRoots:
          "This group has active roots. Review them first and try again",
        expectedGroupName: "Expected: {{groupName}}",
        organizationNotExists: "Target organization does not exist",
        squadOnlyIfContinuous:
          "Squad is only available in groups of type Continuous-Hacking",
        userNotInOrganization:
          "User is not a member of the target organization",
      },
      forces: "DevSecOps agent",
      group: "Group",
      inactive: "Inactive",
      machine: "Machine",
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
        groupFinalization: "Group Finalization",
        groupSuspension: "Group Suspension",
        none: "None",
        observations: "Observations",
        observationsPlaceholder:
          "Please type here any observation you may have",
        other: "Other",
        title: "Change contracted services",
        typeGroupName: "Please type the group name to proceed",
        warning: "Warning",
        warningDowngradeASM:
          "Disabling ASM will immediately delete the group. " +
          "This will remove all of its data including findings and related vulnerabilities. " +
          "This is a destructive action and cannot be undone.",
      },
      oneShot: "One-Shot Hacking",
      oneshot: "One-Shot Hacking",
      service: "Service",
      services: "Services",
      squad: "Squad",
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
          "If you do not have more groups, you will be removed from ASM. ",
        warningTitle: "Warning!",
      },
      white: "White",
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
      acceptanceJustification: "Acceptance Justification",
      acceptanceUser: "Acceptance User",
      action: "Action",
      affectedSystems: {
        text: "Affected systems",
        tooltip: "Project or application that contains the vulnerability",
      },
      approvalMessage:
        "Remember that the indefinite acceptance of a finding requires the approval of a user with manager role",
      approvalTitle: "Confirmation",
      approve: "Approve",
      approveAll: "Approve all",
      approveAllVulns: "Approve all pending vulnerabilities",
      assigned: "Assigned",
      attackVectors: {
        text: "Impacts",
        tooltip:
          "Malicious actions that can be performed by exploiting the vulnerability",
      },
      bts: "External BTS",
      btsPlaceholder: "https://gitlab.com/fluidattacks/asm/-/issues/2084",
      businessCriticality: "Level",
      cancelVerified: "Cancel",
      cancelVerify: "Cancel",
      delete: "Delete",
      deleteAll: "Delete All",
      deleteAllVulns: "Delete all pending vulnerabilities",
      deleteTags: "Delete Tags",
      description: {
        infoLinkText: "Learn more...",
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
      hacker: "Hacker",
      handleAcceptanceModal: {
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
        loadingText: "Loading requirements...",
        text: "Requirements",
        tooltip:
          "Rules that are broken and lead to the existence of the vulnerability",
      },
      risk: "Risk",
      save: {
        text: "Save",
        tooltip: "Save changes",
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
        acceptedUndefined: "Permanently accepted",
        approvedBy: "Approved by",
        confirmRejectZeroRisk: "Confirm/Reject zero risk",
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
      updateVulnerabilities: "Update Vulnerabilities",
      updateVulnerabilitiesTooltip:
        "Modify the existing vulnerabilities using the selected yaml file",
      verification: "Verification",
      vulnApproval: "Vulnerability approval status was changed",
      vulnDeleted: "Vulnerability deleted",
      where: "Where",
      zeroRisk: "Zero risk",
    },
    tabEvents: {
      accessibility: "Accessibility",
      actionAfterBlocking: "Action after blocking",
      actionAfterBlockingValues: {
        none: "None",
        other: "Other",
        otherOther: "Execute another group of a different client",
        otherSame: "Execute another group of the same client",
        training: "Training",
      },
      actionBeforeBlocking: "Action before blocking",
      actionBeforeBlockingValues: {
        documentGroup: "Document group",
        none: "None",
        other: "Other",
        testOtherPartToe: "Test other part ToE",
      },
      affectation: "Affectation",
      affectedComponents: "Affected components",
      affectedComponentsValues: {
        clientStation: "Client's test station",
        compileError: "Compilation error",
        documentation: "Project documentation",
        fluidStation: "FLUID's test station",
        internetConnection: "Internet connectivity",
        localConnection: "Local connectivity (LAN, WiFi)",
        other: "Other(s)",
        sourceCode: "Source code",
        testData: "Test data",
        toeAlteration: "ToE alteration",
        toeCredentials: "ToE credentials",
        toeExclussion: "ToE exclusion",
        toeLocation: "ToE location (IP, URL)",
        toePrivileges: "ToE privileges",
        toeUnaccessible: "ToE inaccessible",
        toeUnavailable: "ToE unavailable",
        toeUnstable: "Unstable ToE",
        vpnConnection: "VPN connectivity",
      },
      client: "Client",
      closingDate: "Closing date",
      comments: "Comments",
      date: "Date",
      description: "Description",
      edit: "Edit",
      eventIn: "Event present in",
      evidence: "Evidence",
      fluidGroup: "Fluid Attacks' Group",
      hacker: "Hacker",
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
      tags: {
        modalTitle: "Add tags information",
      },
    },
    tabMachine: {
      errorNoCheck: "There is no Machine type for this finding",
      headerDuration: "Duration (hh:mm:ss)",
      headerPriority: "Priority",
      headerRoot: "Root",
      headerStartedAt: "Started At",
      headerStatus: "Status",
      priorityHigh: "High",
      priorityNormal: "Normal",
      submitJob: "Queue a Job",
      submitJobSuccess: "Successfully queued job",
      submitting: "Submitting Job, please wait",
      success: "Success",
      tabTitle: "Machine",
      tooltip: "Information about your Machine plan",
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
        fileIsPending:
          "The uploaded file is pending for a scan, you will be notified " +
          "via email once the file is available, or if there is an issue with it",
        title: "Files",
      },
      groupToRemove: "Please type: <strong>{{groupName}}</strong>, to proceed",
      https: "HTTPS",
      information: {
        btnTooltip: "Edit general information of this group",
      },
      invalidChars: "File name has invalid characters.",
      modalEditGroupInformation: "Edit group information",
      modalEnvTitle: "Add environment information",
      modalFileIsPending: "File Pending",
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
      accepted: "temporarily accepted",
      acceptedUndefined: "Permanently accepted",
      assigned: "Assigned:",
      closed: "Closed",
      cycle: "Cycle",
      effectiveness: "Effectiveness",
      found: "Found",
      inProgress: "In progress",
      justification: "Justification:",
      new: "New",
      open: "Open",
      pending: "Pending",
      status: "Status",
      tabTitle: "Tracking",
      tooltip:
        "Evolution of the finding over time: historical records, open/closed vulnerabilities, " +
        "and temporarily/permanently accepted treatments",
      treatment: "Treatment",
      vulnerabilitiesAcceptedTreatment:
        "{{count}} vulnerabilities were temporarily accepted",
      vulnerabilitiesAcceptedUndefinedTreatment:
        "{{count}} vulnerabilities were permanently accepted",
      vulnerabilitiesClosed: "Vulnerabilities closed:",
      vulnerabilitiesFound: "Vulnerabilities found:",
    },
    tabUsers: {
      addButton: {
        text: "Add",
        tooltip: "Add a user to this group",
      },
      editButton: {
        text: "Edit",
        tooltip: "Select a user and edit their information",
      },
      editStakeholderTitle: "Edit stakeholder information",
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
        acceptanceNotRequested: "Indefinite acceptance is not requested",
        acceptanceSuccess: "Indefinite acceptance has been handled",
        hasNewVulns:
          "The treatment is set as new, please select a treatment for the vulnerability.",
        // eslint-disable-next-line camelcase -- It is required for react-i18next
        hasNewVulns_plural:
          "The treatment on one or more vulnerabilities is set as new, please select a treatment for the vulnerabilities.",
        maximumNumberOfAcceptances:
          "Vulnerability has been accepted the maximum number of times allowed by the organization",
        tagReminder:
          "Remember to add tags to your vulnerabilities to ease their management",
        treatmentChange: "Vulnerability treatment will be changed",
        uploadFile: {
          invalidRoot:
            "Active root not found for the repo. Verify the nickname in the scope tab",
          invalidStream: "Invalid stream, it must start with 'home' or 'query'",
          key: "Key '{{key}}' is missing or invalid. ",
          value: "Value is invalid, pattern '{{pattern}}'. ",
        },
      },
      buttons: {
        edit: "Edit",
        handleAcceptance: "Treatment Acceptance",
        reattack: "Reattack",
      },
      buttonsTooltip: {
        cancel: "Cancel",
        edit: "Modify the fields of the vulnerabilities",
        handleAcceptance: "Approve/Reject treatment",
      },
      close: "Close",
      closed: "Closed",
      commitHash: "Commit hash",
      contentTab: {
        details: {
          title: "Details",
          tooltip: "Details",
        },
        tracking: {
          requestApproval: "Approval: ",
          requestDate: "Request date: ",
          title: "Tracking",
          tooltip: "Evolution of the vulnerability treatment over time",
        },
        treatments: {
          title: "Treatments",
          tooltip: "Modify the treatment of the vulnerability",
        },
      },
      errors: {
        selectedVulnerabilities:
          "There were selected vulnerabilities that do not apply",
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
      searchTag: "Search Tag",
      searchText: "Search Text",
      status: "Status",
      statusTooltip:
        "Filter vulnerabilities based on their open / closed status",
      tabTitle: "Locations",
      tagTooltip: "Filter vulnerabilities based on their tag",
      tooltip: "Open / Closed vulnerabilities",
      treatmentStatus:
        "Filter vulnerabilities based on permanently accepted treatment acceptances",
      verified: "Verified",
      vulnTable: {
        assigned: "Assigned",
        currentTreatment: "Current",
        cycles: "Cycles",
        dateTooltip: "Filter vulnerabilities based on the report date",
        efficacy: "Efficiency",
        info: "Info",
        lastReattackDate: "Last reattack date",
        lastRequestedReattackDate: "Last request",
        location: "Location",
        more: "...",
        reattack: "Reattack: ",
        reattacks: "Reattacks",
        reattacksTooltip:
          "Filter vulnerabilities based on the status of their reattack requests",
        report: "Report: ",
        reportDate: "Report date",
        requester: "Requester",
        specific: "Specific",
        specificType: {
          app: "Input",
          code: "LoC",
          infra: "Port",
        },
        status: "Status: ",
        treatmentChanges: "Changes",
        treatmentDate: "Date",
        treatmentExpiration: "Expiration",
        treatmentJustification: "Justification",
        treatments: "Treatments",
        treatmentsTooltip:
          "Filter vulnerabilities based on the treatment they were given",
        verification: "Last reattack",
        vulnerabilityType: {
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
      resendEmail: "Resend",
      userOrganization: "Organization",
      userResponsibility: "Responsibility",
      userRole: "Role",
      usermail: "Stakeholder email",
    },
  },
  sidebar: {
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
      text: "New...",
      tooltip: "Create new organization",
    },
  },
  tagIndicator: {
    acceptedVulnerabilitiesBySeverity: "Accepted vulnerabilities by severity",
    acceptedVulnerabilitiesByUser: "Accepted vulnerabilities by user",
    findingsGroup: "Findings by group",
    meanRemediate: "Mean (average) days to remediate",
    openFindingsGroup: "Open findings by group",
    openVulnsGroups: "Open vulnerabilities by group",
    remediatedAcceptedVuln:
      "How many vulnerabilities are remediated and accepted?",
    remediatedVuln: "How many vulnerabilities are remediated (closed)?",
    topOldestFindings: "Top oldest findings",
    undefinedTitle: "Treatmentless by group",
    vulnerabilitiesByLevel: "Vulnerabilities by level",
    vulnerabilitiesByTag: "Vulnerabilities by tag",
    vulnerabilitiesByTreatments: "Vulnerabilities by treatments",
    vulnerabilitiesByType: "Vulnerabilities by source",
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
    responsibility: "Responsibility",
    responsibilityPlaceholder: "Product Owner, Group Manager, Tester, ...",
    role: "Role",
    roles: {
      admin: "Admin",
      analyst: "Hacker",
      architect: "Architect",
      closer: "Reattacker",
      customer: "User",
      customeradmin: "User Manager",
      executive: "Executive",
      groupManager: "System Owner",
      hacker: "Hacker",
      reattacker: "Reattacker",
      resourcer: "Resourcer",
      reviewer: "Reviewer",
      systemOwner: "System Owner",
    },
    success: "{{email}} was added successfully",
  },
  validations: {
    alphanumeric: "Only alphanumeric characters",
    between: "This value must be between {{min}} and {{max}}",
    columns: "At least 1 column must be shown",
    datetime: "The datetime format is not valid",
    datetimeBetween: "The datetime must be between {{from}} and {{to}}",
    draftTitle: "The title format is not valid",
    draftTypology: "The finding typology is not valid",
    duplicateDraft:
      "A {{type}} of this type has been already created. Please submit vulnerabilities there",
    email: "The email format is not valid",
    excludeFormat: "Root name should not be included in the exception pattern",
    fileSize: "The file size must be less than {{count}}MB",
    fluidAttacksStaffWithoutFluidAttacksService:
      "Groups without an active Fluid Attacks service " +
      "can not have Fluid Attacks staff",
    greaterDate: "The date must be today or before",
    inactiveSession:
      "You will be logged out for inactivity in a minute. Click on Dismiss if you wish to stay logged in.",
    inactiveSessionDismiss: "Dismiss",
    inactiveSessionModal: "Inactive Session Detected",
    infectedFile: "Our system detected that the uploaded file is infected",
    invalidChar:
      "Invalid characters, use: alphanumerics, spaces and punctuations",
    invalidCommentParent: "The comment parent is invalid",
    invalidEmailInField: "The email address inserted is not valid",
    invalidFieldLength: "The value inserted in one of the fields is too large",
    invalidMarkdown: "Invalid or malformed markdown",
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
    oneOf: "This field must be one of the suggested values",
    positive: "The number must be greater than 0",
    requireNickname: "Nickname already exist",
    required: "Required field",
    someRequired: "Select at least one value",
    stakeholderHasGroupAccess:
      "The stakeholder has been granted access to the group previously",
    tags: "This field can only contain alphanumeric characters and dashes",
    userIsNotFromFluidAttacks:
      "This role can only be granted to Fluid Attacks users",
    validDate: "The date must be below six months",
    validDateToken: "The date must be below six months",
    validSessionDate: "The session has expired",
  },
};

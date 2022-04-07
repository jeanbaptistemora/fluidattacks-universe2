import type { ResourceKey } from "i18next";

export const enTranslations: ResourceKey = {
  analytics: {
    barChart: {
      eventualities: "Unsolved events by groups",
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
      all: {
        text: "All",
        tooltip: "All data, not filtered",
      },
      ninetyDays: {
        text: "90",
        tooltip: "Data filtered from the last 90 days",
      },
      thirtyDays: {
        text: "30",
        tooltip: "Data filtered from the last 30 days",
      },
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
        title: "Agent",
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
      daysUntilZeroExposition: {
        title: "Days until zero exposure",
      },
      findingsBeingReattacked: {
        title: "Vulnerabilities being re-attacked",
      },
      forcesRepositoriesAndBranches: {
        title: "Repositories and branches",
      },
      forcesStatus: {
        footer: {
          breaks:
            "In case the DevSecOps agent finds one vulnerability to be open, " +
            "we can (optionally) mark the build as failed, so you never " +
            "introduce known vulnerabilities into the production environment. " +
            "This strict mode can be customized with severity thresholds and " +
            "grace periods to be tailored to your needs.",
          intro:
            "By enabling DevSecOps you get access to a Docker container built " +
            "to specifically verify the status of security findings in your system. " +
            "You can embed this container in your Continuous Integration system " +
            "to test for changes in security vulnerabilities:",
          smart:
            "DevSecOps is fast and automatic, as it is created by the same intelligence " +
            "of the hackers who already know your system in-depth, it can therefore " +
            "verify the attack vectors as no other tools can.",
          stats:
            "Statistics from over a hundred different systems show that DevSecOps " +
            "increases the remediation ratio, helping you to build a safer system " +
            "and to be more cost-effective throughout your Software " +
            "Security Development Life Cycle.",
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
  app: {
    minimumWidth: "ASM is only available on desktops",
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
  deleteVulns: {
    closedVuln: "A closed vulnerability cannot be removed",
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
        invitation: "Filter by invitation",
        repository: "Filter by repository",
      },
      groupsContributed: "Groups Contributed",
      invitationState: {
        confirmed: "Registered",
        pending: "Pending",
        unregistered: "Non-registered",
      },
      repository: "Repository",
      sendInvitation: "Invite",
      tableAdvice:
        "Below you'll find the authors that have contributed " +
        "to your group in the selected month, and one example commit",
      tooltip: {
        text: "Send group invitation to non-registered author",
      },
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
          holds:
            "{{ length }} reattack(s) put on hold by this Event " +
            "will be set to Requested",
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
        affectedReattacks: {
          alreadyClosed:
            "At least one of the selected reattacks was closed already",
          alreadyOnHold:
            "At least one of the selected reattacks was put on hold already",
          btn: {
            text: "Update Affected Reattacks",
            tooltip: "Put reattacks on hold on already existing Events",
          },
          checkbox: "Does this event have an impact on any ongoing reattacks?",
          description: "Please select the affected reattacks",
          eventSection: "Event",
          holdsCreate: "Reattack holds requested successfully",
          sectionTitle: "Affected Reattacks",
          selection: "Please select the reattacks that would be affected",
          title: "Update Affected Reattacks",
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
        invalidFileName: "Evidence filename must not have invalid chars",
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
      headersTooltips: {
        lastReport: "Number of days since the last vulnerability was added",
        locations: "Number of instances of the vulnerability",
        reattack: "Current reattack status",
        severity: "Risk scoring according to CVSS 3.1",
        status:
          "Current state of the vulnerability: Open if the vulnerabilty persists, " +
          "Closed if it was solved",
        type: "Vulnerability title",
        where: "Exact location of the vulnerability.",
      },
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
        cert: "  Certificate",
        certTooltip:
          "Receive a security testing certification with the up-to-date" +
          " Finding remediation data of this group. Before requesting it," +
          " make sure to fill out the Information section of Scope",
        data: "  Export",
        dataTooltip:
          "Receive a zip file containing the exported data of all the findings " +
          "of this group",
        filterReportDescription:
          "Here you can customize the length of the report " +
          "by selecting these fields",
        generateXls: "Generate XLS",
        modalClose: "Close",
        modalTitle: "Reports",
        noMobileAppWarning:
          "Reports are created on-demand and are protected by a <strong>passphrase</strong>. " +
          "The <strong>passphrase</strong> is generated randomly and will be " +
          "sent through a notification to your mobile device. In order to receive it, " +
          "you will need to download and set up the ASM mobile app, please " +
          "download it and try again.",
        passphraseOptOut: "If you want remove passphrase protection, follow",
        pdf: "  Executive",
        pdfTooltip:
          "Receive a pdf file with an executive report that gives you summarized information " +
          "about all the findings of this group",
        techDescription:
          "Reports are created on-demand and are protected by a <strong>passphrase</strong>. " +
          "The <strong>passphrase</strong> is generated randomly and will be " +
          "sent through a notification to your mobile device.",
        treatment: "Treatment",
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
      gracePeriod: {
        title: "Grace Period",
      },
      identifier: "Identifier",
      kind: {
        all: "ALL",
        dynamic: "DAST",
        other: "ALL",
        static: "SAST",
        title: "Type",
      },
      severityThreshold: {
        title: "Severity Threshold",
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
          other: "What?",
          reason: {
            label: "Reason",
            mistake: "Registered by mistake",
            moved: "Moved to another group",
            other: "Other",
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
            "An active root with the same URL/Branch already exists " +
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
          invalidGitCredentials:
            "Git repository was not accessible with given credentials",
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
          healthCheck: {
            placeholder: "Health Check",
            text: "Filter if health check is included for existing code",
          },
          nickname: "Filter by nickname",
          state: "Filter by state",
          status: "Filter by status",
        },
        healthCheck: {
          accept: "I accept the additional costs derived from the healthcheck",
          confirm: "Would you like a health check for the existing code?",
          no: "No",
          rejectA:
            "I accept that Fluid Attacks will not include a revision of the existing code in the repository",
          rejectB:
            "I accept that the existing code contains vulnerabilities that will not be detected",
          rejectC:
            "I accept that the previously defined SLAs do not apply to this repository",
          tableHeader: "HCK",
          title: "Health Check",
          titleTooltip: "Health check include for existing code",
          yes: "Yes",
        },
        manageEnvs: "Manage environments",
        manageEnvsTooltip:
          "Add, edit or remove environment URLs for the selected git root",
        repo: {
          branch: "Branch",
          cloning: {
            message: "Message",
            status: "Status",
            sync: "Sync",
          },
          credentials: {
            checkAccess: {
              noAccess: "Credentials are invalid",
              success: "Repository was reached successfully",
              successTitle: "Success",
              text: "Check Access",
            },
            https: "HTTPS",
            name: "Credential Name",
            nameHint: "Repository SSH Key",
            password: "Repository password",
            secrets: {
              add: "Add secret",
              description: "Secret description",
              key: "Key",
              remove: "Remove",
              removed: "removed",
              success: "added secret",
              successTitle: "Success",
              tittle: "Secrets management",
              update: "Update secret",
              value: "Value",
            },
            ssh: "SSH",
            sshHint:
              "-----BEGIN OPENSSH PRIVATE KEY-----\n" +
              "SSH PRIVATE KEY...\n" +
              "-----END OPENSSH PRIVATE KEY-----",
            sshKey: "Private SSH Key",
            token: "Repository access token",
            type: "Credential Type",
            user: "Repository user",
          },
          environment: "Environment kind",
          environmentHint: "(Production, QA or other)",
          machineExecutions: {
            active: "There is an active analysis in progress",
            messageComplete: "Last complete Machine execution",
            messageSpecific: "Last finding reattacked",
            noExecutions: "There are no executions yet",
          },
          nickname: "Nickname",
          nicknameHint:
            "Nickname must be unique and different from the repository name",
          title: "Git repository",
          url: "URL",
          useVpn: "Use Vpn",
        },
        sync: {
          alreadyCloning: "Git root already has an active cloning process",
          noCredentials:
            "Git root cannot be cloned due to lack of access credentials",
          success: "Sync started successfully",
          successTitle: "Success",
        },
        title: "Git Roots",
      },
      internalSurface: {
        confirmDialog: {
          title: "Internal surface",
        },
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
        actionButtons: {
          addButton: {
            text: "Add",
            tooltip: "Add new input",
          },
          cancelButton: {
            text: "Cancel",
            tooltip: "Cancel",
          },
          editButton: {
            text: "Edit",
            tooltip: "Edit input",
          },
          removeButton: {
            text: "Remove",
            tooltip: "Remove non-enumerated input",
          },
        },
        addModal: {
          alerts: {
            alreadyExists: "The input already exists.",
            invalidComponent: "The root does not have the component.",
            invalidUrl: "The URL is not valid.",
            success: "Input has been added.",
          },
          close: "Close",
          fields: {
            component: "Component",
            entryPoint: "Entry point",
            environmentUrl: "Environment url",
            path: "Path",
            root: "Root",
          },
          procced: "Proceed",
          title: "Add input",
        },
        attackedAt: "Attacked at",
        attackedBy: "Attacked by",
        bePresent: "Be present",
        bePresentUntil: "Be present until",
        commit: "Commit",
        component: "Component",
        editModal: {
          alerts: {
            alreadyUpdate: "Something modified the input during the edition.",
            invalidAttackedAt:
              "The attacked at is not valid. There is a new datetime.",
            nonPresent: "The input is not present.",
            success: "Input has been updated.",
          },
          close: "Close",
          fields: {
            bePresent: "Be present",
            hasRecentAttack: "Has it been attacked recently?",
          },
          procced: "Proceed",
          title: "Edit input",
        },
        entryPoint: "Entry point",
        filters: {
          bePresent: {
            placeholder: "Be present (refetch)",
            tooltip: "Filter by be present",
          },
          component: {
            placeholder: "Component",
            tooltip: "Filter by component",
          },
          hasVulnerabilities: {
            placeholder: "Has vulnerabilities",
            tooltip: "Filter by has vulnerabilities",
          },
          root: {
            placeholder: "Root (refetch)",
            tooltip: "Filter by root",
          },
          seenAt: {
            placeholder: "Seen at (range)",
            tooltip: "Filter by seen at",
          },
          seenFirstTimeBy: {
            placeholder: "Seen first time by",
            tooltip: "Filter by seen first time by",
          },
        },
        firstAttackAt: "First attack at",
        hasVulnerabilities: "Has vulnerabilities",
        no: "No",
        remove: {
          alerts: {
            success: "Input has been removed.",
          },
        },
        root: "Root",
        seenAt: "Seen at",
        seenFirstTimeBy: "Seen first time by",
        yes: "Yes",
      },
      lines: {
        actionButtons: {
          editButton: {
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
        filters: {
          bePresent: {
            placeholder: "Be present (refetch)",
            tooltip: "Filter by be present",
          },
          coverage: {
            placeholder: "Coverage % (range)",
            tooltip: "Filter by coverage %",
          },
          extension: {
            placeholder: "Extension",
            tooltip: "Filter by extension",
          },
          hasVulnerabilities: {
            placeholder: "Has vulnerabilities",
            tooltip: "Filter by has vulnerabilities",
          },
          modifiedDate: {
            placeholder: "Modified date (range)",
            tooltip: "Filter by modified date",
          },
          priority: {
            placeholder: "Priority % (range)",
            tooltip: "Filter by priority %",
          },
          root: {
            placeholder: "Root (refetch)",
            tooltip: "Filter by root",
          },
          seenAt: {
            placeholder: "Seen at (range)",
            tooltip: "Filter by seen at",
          },
        },
        firstAttackAt: "First attack at",
        hasVulnerabilities: "Has vulnerabilities",
        lastAuthor: "Last author",
        lastCommit: "Last commit",
        loc: "LOC",
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
    reportAlreadyRequested:
      "Please wait until the already requested report finishes processing before " +
      "requesting a new report for this group",
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
        "classification means that this information is only to be used by those for " +
        "whom it was meant. In case of requiring its total or partial reproduction, this " +
        "must be done with express and written authorization of Fluid Attacks. " +
        "The regulations that limit the use and disclosure of this information are " +
        "article 72 and subsequent articles of Chapter IV of Decision 344 of the " +
        "Cartagena Agreement of 1993, article 270 and subsequent articles " +
        "of Title VIII of the Colombian Penal Code, and article 16 " +
        "and subsequent articles of Law 256 of 1996.",
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
          "This is a destructive action. " +
          "An email will be sent to confirm the deletion.",
        warning: "Warning!",
      },
      requestedTooSoon:
        "Please wait a minute before resending a confirm deletion",
      success: "You'll receive a delete confirmation email shortly",
      successTitle: "Success",
      text: "Delete Account",
      tooltip: "Delete account from ASM",
    },
    help: {
      chat: "Live Chat",
      expert: "Talk to an expert",
    },
    home: {
      text: "Home",
    },
    logout: {
      text: "Log out",
      tooltip: "Log out of ASM",
    },
    mobile: {
      text: "Mobile",
      tooltip: "Manage the mobile information",
    },
    newsTooltip: "Latest updates about ASM",
    notification: {
      text: "Notifications",
      tooltip: "Some settings to the notifications here",
    },
    role: "Role:",
    searchPlaceholder: "Search group",
    task: {
      text: "Todos",
      tooltip: "To-Do List",
    },
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
        groups: {
          title: "Groups",
          updateSubscription: {
            errors: {
              addPaymentMethod: "Please add a payment method first",
              alreadyActive:
                "The group already has a subscription of the chosen type",
              couldNotBeDowngraded:
                "Subscription could not be downgraded, payment intent for Squad failed",
              couldNotBeUpdated:
                "Subscription could not be updated. Please review your invoices",
            },
            subscription: "Subscription",
            success: {
              body: "Group subscription successfully updated",
              title: "Success",
            },
            title: "Update",
            types: {
              free: "Free",
              machine: "Machine",
              squad: "Squad",
            },
          },
        },
        paymentMethods: {
          add: {
            button: "Add",
            errors: {
              alreadyExists:
                "Provided payment method already exists. Please update or delete it first",
              couldNotBeCreated:
                "Payment method could not be created. Please make sure all the details you provided are correct",
            },
            modal: {
              add: "Add payment method",
              cvc: "Card CVC",
              default: "Make card default payment method",
              expirationMonth: "Card expiration month",
              expirationYear: "Card expiration year",
              number: "Card number",
            },
            success: {
              body: "Payment method successfuly added",
              title: "Success",
            },
          },
          defaultPaymentMethod: "(Default)",
          remove: {
            button: "Remove",
            errors: {
              activeSubscriptions:
                "All subscriptions must be cancelled before removing your latest payment method",
              noPaymentMethod: "The payment method does not exist",
            },
            success: {
              body: "Payment method successfully removed",
              title: "Success",
            },
          },
          title: "Payment Methods",
          update: {
            button: "Update",
            modal: {
              default: "Make card default payment method",
              expirationMonth: "Card expiration month",
              expirationYear: "Card expiration year",
              update: "Update payment method",
            },
            success: {
              body: "Payment method successfuly updated",
              title: "Success",
            },
          },
        },
        portal: {
          title: "Invoices",
        },
        text: "Billing",
        tooltip: "Billing and subcriptions for your organization",
      },
      groups: {
        disabled: "Disabled",
        enabled: "Enabled",
        filtersTooltips: {
          groupName: "Filter by group name",
          plan: "Filter by plan",
        },
        newGroup: {
          businessId: {
            text: "Business Registration Number",
            tooltip: "The registration number of your business e.g. NIT",
          },
          businessName: {
            text: "Business Name",
            tooltip: "The name of your business",
          },
          description: {
            text: "Description",
            tooltip: "Brief description to identify the group",
          },
          events: {
            text: "Events",
            tooltip: "There are open eventualities that may affect tests.",
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
          name: "Group name",
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
        plan: "Plan",
        role: "Role",
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
          vulnerabilityGracePeriod:
            "Maximum acceptance days should be a positive integer",
        },
        findings: {
          addPolicies: {
            success:
              "Remember that the application of the policy requires the approval of a user with manager role",
          },
          deactivatePolicies: {
            modalTitle: "Disable organization vulnerability policy",
            success:
              "The vulnerability policy was disabled successfully, changes will be apply it within next minutes",
          },
          errors: {
            alreadyReviewd:
              "The vulnerability policy has already been reviewed",
            duplicateFinding: "The vulnerability policy already exists",
            notFound: "Finding policy not found",
          },
          form: {
            finding: "Vulnerability",
            tags: "Tags",
          },
          handlePolicies: {
            success: {
              approved: "The policy will be applied within the next minutes",
              rejected: "The policy was successfully rejected",
            },
          },
          submitPolicies: {
            modalTitle: "Re-submit organization vulnerability policy",
          },
          title: "Organization Vulnerabilities Policies",
          tooltip: {
            addButton: "Add organization policy pending to approve",
            approveButton: "Approve organization vulnerability policy",
            deactivateButton: "Disable organization vulnerability policy",
            nameInput:
              "Add the type of vulnerability to which locations in organization " +
              "groups will apply the accepted permanently treatment",
            rejectButton: "Reject organization vulnerability policy",
            resubmitButton: "Re-submit organization vulnerability policy",
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
          vulnerabilityGracePeriod:
            "Grace period in days where newly reported vulnerabilities won't " +
            "break the build (DevSecOps only)",
        },
        policy: "Policy",
        recommended: {
          acceptanceDays: "0",
          acceptanceSeverity: "0.0    -    0.0",
          breakableSeverity: "0.0",
          numberAcceptances: "0",
          title: "Recommended Values",
          vulnerabilityGracePeriod: "0",
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
  profile: {
    mobileModal: {
      add: "Add",
      alerts: {
        additionSuccess: "Mobile has been added.",

        editionSuccess: "Mobile has been updated.",

        invalidVerificationCode: "The verification code is invalid",
        nonSentVerificationCode:
          "Check your mobile number and retry in a minute",
        nonVerifiedStakeholder: "Stakeholder could not be verified",
        requiredMobile: "A mobile number is required",
        requiredVerificationCode: "A verification code is required",
        sameMobile: "The new phone number can not be the current phone number",
        sendCurrentMobileVerificationSuccess:
          "A verification code has been sent to your mobile",
        sendNewMobileVerificationSuccess:
          "A verification code has been sent to your new mobile",
      },
      close: "Close",
      edit: "Edit",
      fields: {
        newPhoneNumber: "New phone number",
        phoneNumber: "Phone number",
        verificationCode: "Verification code",
      },
      title: "Mobile",
      verify: "Verify",
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
    draftApproved: "This finding was approved",
    draftStatus: {
      created: "Created",
      rejected: "Rejected",
      submitted: "Submitted",
    },
    enumValues: {
      ACCESS_GRANTED: {
        name: "ACCESS_GRANTED",
        tooltip: "ACCESS_GRANTED",
      },
      CHARTS_REPORT: {
        name: "Analytics report",
        tooltip:
          "Get charts and data on the status and characteristics " +
          "of reported vulnerabilities and your remediation practices.",
      },
      COMMENTS: "Consulting",
      DAILY_DIGEST: {
        name: "Daily digest",
        tooltip:
          "Get daily updates on noteworthy activity and vulnerabilities " +
          "in your subscribed groups.",
      },
      DIGEST: "Daily digest",
      EVENT_REPORT: {
        name: "Event alert",
        tooltip:
          "Get information about an event when it is reported in a group.",
      },
      GROUP: "GROUP",
      GROUP_REPORT: {
        name: "GROUP_REPORT",
        tooltip: "GROUP_REPORT",
      },
      NEW_COMMENT: {
        name: "Consulting",
        tooltip:
          "Get notifications when an ASM user submits a comment concerning " +
          "a group, a specific vulnerability or an event.",
      },
      NEW_DRAFT: {
        name: "Draft updates",
        tooltip:
          "Get notifications when a hacker submits a vulnerability draft " +
          "or when a draft is rejected.",
      },
      ORGANIZATION: "ORGANIZATION",
      PORTFOLIO: "PORTFOLIO",
      REMEDIATE_FINDING: {
        name: "Vulnerability updates",
        tooltip:
          "Get notifications when a new vulnerability is discovered, " +
          "a vulnerability fix is reported " +
          "or a specific vulnerability is removed.",
      },
      ROOT_MOVED: {
        name: "Root updates",
        tooltip:
          "Get notifications when a user deactivates a root " +
          "or moves a root to another group.",
      },
      UPDATED_TREATMENT: {
        name: "Treatment updates",
        tooltip:
          "Get notifications when a user defines how to address a vulnerability.",
      },
      VULNERABILITY_ASSIGNED: {
        name: "Vulnerability assignment",
        tooltip:
          "Get notifications when a user is assigned to work on a vulnerability.",
      },
      VULNERABILITY_REPORT: {
        name: "Vulnerability alert",
        tooltip:
          "Get notifications when a vulnerability is reported or closed.",
      },
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
    header: {
      discoveryDate: {
        label: "First reported",
        tooltip:
          "The year, month, and day we first identified " +
          "and reported this type of vulnerability for this group.",
      },
      estRemediationTime: {
        label: "Est. Remediation Time",
        tooltip:
          "The number of hours we estimate it will take you to remediate this type of vulnerability.",
      },
      openVulns: {
        label: "Open vulnerabilities",
        tooltip:
          "The number of locations in your system that still have this type of vulnerability open.",
      },
      severity: {
        label: "Severity",
        level: {
          critical:
            "The <strong>critical</strong> rating " +
            "is for vulnerabilities that can lead to an extreme impact on an organization. " +
            "Exploitation likely results in root-level compromise of servers or infrastructure. " +
            "Attackers do not need special authentication credentials or knowledge about individual victims.",
          high:
            "The <strong>high</strong> rating " +
            "is for vulnerabilities that can lead to an elevated impact on an organization. " +
            "Exploitation can be difficult and can result in elevated privileges " +
            "as well as significant data loss or downtime for the victim.",
          low:
            "The <strong>low</strong> rating " +
            "is for vulnerabilities that can lead to a minimal impact on an organization. " +
            "Exploitation usually requires local or physical system access.",
          medium:
            "The <strong>medium</strong> rating " +
            "is for vulnerabilities that can lead to a moderate impact on an organization. " +
            "Exploitation requires user privileges, and sometimes " +
            "that the attackers reside on the same local network as their victim. It only provides minimal access.",
          none:
            "<The <strong>none</strong> rating " +
            "is for vulnerabilities that cannot lead to an impact on an organization.",
        },
        tooltip: "The severity level is based on the CVSS. ",
      },
      status: {
        label: "Status",
        stateLabel: {
          closed: "Closed",
          open: "Open",
        },
        stateTooltip: {
          closed:
            "The <strong>closed</strong> status means that " +
            "you remediated this type of vulnerability at each location where we reported it.",
          open:
            "The <strong>open</strong> status means that " +
            "you have not remediated this type of vulnerability in at least one of the locations where it has been reported.",
        },
        tooltip: "",
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
    notificationTable: {
      email: "Email",
      notification: "Notification",
      push: "Push",
      sms: "SMS",
      voice: "Voice",
      whatsapp: "Whatsapp",
    },
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
      notification: {
        emailNotificationError:
          "There was an error sending the email notification to the assigned",
        emailNotificationText: "Assigned email notification sent successfully",
        emailNotificationTitle: "Notification Status",
      },
      old: "Old",
      path: "Path",
      port: "Port",
      portPlural: "Ports",
      recommendation: {
        text: "Recommendation",
        tooltip: "General suggestion to solve the vulnerability",
      },
      remediationModal: {
        globalSwitch: {
          text: "Change all",
          tooltip: "Toggle the state change for all vulnerabilities",
        },
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
      checkAll: "Check all roots",
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
      attackComplexity: {
        label: "Attack Complexity",
        options: {
          high: {
            label: "High",
            tooltip:
              "<strong>High (H)</strong><br>" +
              "A successful attack cannot be achieved at will. " +
              "Instead, it requires the attacker to spend a measurable amount of effort, " +
              "preparing or executing against the vulnerable component, " +
              "before a successful attack can be expected.",
          },
          low: {
            label: "Low",
            tooltip:
              "<strong>Low  (L)</strong><br>" +
              "There are no special access conditions or extenuating circumstances. " +
              "An attacker can expect repeatable success by attacking the vulnerable component.",
          },
        },
        tooltip:
          "<strong><big>Attack Complexity (AC)</big></strong><br>" +
          "Describes the conditions outside the attacker's control that must exist in order to exploit the vulnerability. " +
          "Such conditions may require the collection of more information about the target or computational exceptions.",
      },
      attackVector: {
        label: "Attack Vector",
        options: {
          adjacent: {
            label: "Adjacent network",
            tooltip:
              "<strong>Adjacent (A)</strong><br>" +
              "The vulnerable component is bound to the network stack, " +
              "but the attack is limited at the protocol level to a logically adjacent topology. " +
              "This may mean that an attack must be launched from the same shared physical or logical network, " +
              "or from within a limited or secure administrative domain.",
          },
          local: {
            label: "Local",
            tooltip:
              "<strong>Local (L)</strong><br>" +
              "The vulnerable component is not bound to the network stack. " +
              "The attacker exploits the vulnerability by accessing it locally (eg, keyboard, console), remotely (eg, SSH), " +
              "or by relying on user interaction with another person to perform the actions necessary to exploit the vulnerability.",
          },
          network: {
            label: "Network",
            tooltip:
              "<strong>Network (N)</strong><br>" +
              "The vulnerable component is bound to the network stack and includes the entire Internet. " +
              "Such vulnerability is often referred as a remote exploitable and, " +
              "can be thought of as an attack exploitable at the protocol level one or more network hops away.",
          },
          physical: {
            label: "Physical",
            tooltip:
              "<strong>Physical (P)</strong><br>" +
              "The attack requires the attacker to physically touch or manipulate the vulnerable component. " +
              "The physical interaction can be brief or persistent.",
          },
        },
        tooltip:
          "<strong><big>Attack Vector (AV)</big></strong><br>" +
          "It reflects the context in which the exploitation of vulnerabilities is possible. " +
          "This metric value will be higher the more remote (logically and physically) an attacker can be to exploit the vulnerable component.",
      },
      authentication: "Authentication",
      authenticationOptions: {
        multipleAuth: "Multiple: Multiple authentication points",
        noAuth: "None: Authentication is not required",
        singleAuth: "Single: Single authentication point",
      },
      availabilityImpact: {
        label: "Availability Impact",
        options: {
          high: {
            label: "High",
            tooltip:
              "<strong>High (H)</strong><br>" +
              "It is a total loss of availability, " +
              "which makes it possible for the attacker to completely deny access to resources on the impacted component. " +
              "Alternatively, the attacker has the ability to deny some availability, " +
              "but the loss of availability presents a direct and serious consequence for the impacted component.",
          },
          low: {
            label: "Low",
            tooltip:
              "<strong>Low (L)</strong><br>" +
              "Performance is reduced or there are interruptions in the availability of resources. " +
              "Even if repeated exploitation of the vulnerability is possible, " +
              "the attacker does not have the ability to completely deny service to legitimate users. " +
              "Often there are no direct and serious consequences for the impacted component.",
          },
          none: {
            label: "None",
            tooltip:
              "<strong>None (N)</strong><br>" +
              "There is no impact to availability within the impacted component.",
          },
        },
        tooltip:
          "<strong><big>Availability (A)</big></strong><br>" +
          "It measures the impact on the availability of the affected component such as a network service " +
          "(eg, web, database, email). It refers to the accessibility of information resources, " +
          "attacks that consume network bandwidth, processor cycles or disk space can affect availability.",
      },
      availabilityRequirement: {
        label: "Availability Requirement",
        options: {
          high: {
            label: "High",
          },
          low: {
            label: "Low",
          },
          medium: {
            label: "Medium",
          },
        },
      },
      confidentialityImpact: {
        label: "Confidentiality Impact",
        options: {
          high: {
            label: "High",
            tooltip:
              "<strong>High (H)</strong><br>" +
              "There is a complete loss of confidentiality, " +
              "resulting in all resources within the impacted component being disclosed to the attacker. Alternatively, " +
              "only certain restricted information is accessed, but the information disclosed has a direct and serious impact.",
          },
          low: {
            label: "Low",
            tooltip:
              "<strong>Low (L)</strong><br>" +
              "There is some loss of confidentiality. Some restricted information is accessed, " +
              "but the attacker has no control over what information is obtained, or the amount or type of loss is limited. " +
              "The disclosure of information does not cause a direct and serious loss to the impacted component.",
          },
          none: {
            label: "None",
            tooltip:
              "<strong>None (N)</strong><br>" +
              "There is no loss of confidentiality within the impacted component.",
          },
        },
        tooltip:
          "<strong><big>Confidentiality (C)</big></strong><br>" +
          "Measures the impact on the confidentiality of information resources " +
          "managed by a software component due to a successfully exploited vulnerability. " +
          "Confidentiality refers to limiting access and disclosure of information to authorized users only, " +
          "as well as preventing access or disclosure to unauthorized persons.",
      },
      confidentialityRequirement: {
        label: "Confidentiality Requirement",
        options: {
          high: {
            label: "High",
          },
          low: {
            label: "Low",
          },
          medium: {
            label: "Medium",
          },
        },
      },
      cvssVersion: "CVSS Version",
      editable: {
        label: "Edit",
        tooltip: "Modify severity metrics",
      },
      exploitability: {
        label: "Exploitability",
        options: {
          conceptual: {
            label: "Conceptual",
          },
          functional: {
            label: "Functional",
            tooltip:
              "<strong>Functional (F)</strong><br>" +
              "Functional exploit code is available. The code works in most situations where the vulnerability exists.",
          },
          high: {
            label: "High",
            tooltip:
              "<strong>High (H)</strong><br>" +
              "Functional autonomous code exists, or no exploit is required (manual trigger). " +
              "Such code works in all situations or is actively delivered through an autonomous agent " +
              "(such as a worm or virus). Exploit development has reached the level of reliable, " +
              "widely available, and easy-to-use automated tools.",
          },
          improbable: {
            label: "Improbable",
          },
          proofOfConcept: {
            label: "Proof of Concept",
            tooltip:
              "<strong>Proof-of-Concept (P)</strong><br>" +
              "Proof-of-concept exploit code is available, " +
              "or an attack demonstration is not practical for most systems. " +
              "The code or technique is not functional in all situations and " +
              "may require substantial modification by a skilled attacker.",
          },
          unproven: {
            label: "Unproven",
            tooltip:
              "<strong>Unproven (U)</strong><br>" +
              "No exploit code is available, or an exploit is theoretical.",
          },
        },
        tooltip:
          "<strong><big>Exploitability (E)</big></strong><br>" +
          "It measures the likelihood that the vulnerability will be attacked, " +
          "and is typically based on the current state of exploitation techniques, " +
          "the availability of exploit code, or active “in-the-wild” exploitation.",
      },
      integrityImpact: {
        label: "Integrity Impact",
        options: {
          high: {
            label: "High",
            tooltip:
              "<strong>High (H):</strong><br>" +
              "There is a total loss of integrity, or a complete loss of protection. " +
              "The attacker is able to modify some or any/all data protected by the impacted component. " +
              "A malicious modification would present a direct, serious consequence to the impacted component.",
          },
          low: {
            label: "Low",
            tooltip:
              "<strong>Low (L)</strong><br>" +
              "Modification of data is possible, " +
              "but the attacker does not have control over the consequence of a modification, " +
              "or the amount of modification is limited. " +
              "The data modification does not have a direct, serious impact on the impacted component.",
          },
          none: {
            label: "None",
            tooltip:
              "<strong>None (N)</strong><br>" +
              "There is no loss of integrity within the impacted component.",
          },
        },
        tooltip:
          "<strong><big>Integrity (I)</big></strong><br>" +
          "Measures the impact to integrity of a successfully exploited vulnerability. " +
          "Integrity refers to the trustworthiness and veracity of information.",
      },
      integrityRequirement: {
        label: "Integrity Requirement",
        options: {
          high: {
            label: "High",
          },
          low: {
            label: "Low",
          },
          medium: {
            label: "Medium",
          },
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
      privilegesRequired: {
        label: "Privileges Required",
        options: {
          high: {
            label: "High",
            tooltip:
              "<strong>High (H)</strong><br>" +
              "The attacker requires privileges that provide significant (eg, administrative) " +
              "control over the vulnerable component allowing access to component-wide settings and files.",
          },
          low: {
            label: "Low",
            tooltip:
              "<strong>Low (L)</strong><br>" +
              "The attacker requires privileges that provide basic user capabilities " +
              "that could normally affect only settings and files owned by a user. Alternatively, " +
              "an attacker with Low privileges has the ability to access only non-sensitive resources.",
          },
          none: {
            label: "None",
            tooltip:
              "<strong>None (N)</strong><br>" +
              "The attacker is unauthorized prior to attack, and therefore, " +
              "does not require any access to settings or files of the vulnerable system to carry out an attack.",
          },
        },
        tooltip:
          "<strong><big>Privileges Required (PR)</big></strong><br>" +
          "This metric describes the level of privileges an attacker must possess before successfully exploiting the vulnerability. " +
          "The Base Score is greatest if no privileges are required.",
      },
      remediationLevel: {
        label: "Remediation Level",
        options: {
          officialFix: {
            label: "Official Fix",
            tooltip:
              "<strong>Official Fix (O)</strong><br>" +
              "A complete vendor solution is available. " +
              "Either the vendor has issued an official patch, or an upgrade is available.",
          },
          temporaryFix: {
            label: "Temporary Fix",
            tooltip:
              "<strong>Temporary Fix (T)</strong><br>" +
              "There is an official but temporary fix available. " +
              "This includes instances where the vendor issues a temporary hotfix, tool, or workaround.",
          },
          unavailable: {
            label: "Unavailable",
            tooltip:
              "<strong>Unavailable (U)</strong><br>" +
              "There is either no solution available or it is impossible to apply.",
          },
          workaround: {
            label: "Workaround",
            tooltip:
              "<strong>Workaround (W)</strong><br>" +
              "There is an unofficial, non-vendor solution available. In some cases, " +
              "users of the affected technology will create a patch of their own " +
              "or provide steps to work around or otherwise mitigate the vulnerability.",
          },
        },
        tooltip:
          "<strong><big>Remediation Level (RL)</big></strong><br>" +
          "It is an important factor for prioritization. " +
          "The typical vulnerability is unpatched when initially published. " +
          "Workarounds or hotfixes may offer interim remediation until an official patch or upgrade is issued.",
      },
      reportConfidence: {
        label: "Report Confidence",
        options: {
          confirmed: {
            label: "Confirmed",
            tooltip:
              "<strong>Confirmed (C)</strong><br>" +
              "Detailed reports exist, or functional reproduction is possible. " +
              "Source code is available to independently verify the assertions of the research, " +
              "or the author or vendor of the affected code has confirmed the presence of the vulnerability.",
          },
          reasonable: {
            label: "Reasonable",
            tooltip:
              "<strong>Reasonable (R)</strong><br>" +
              "Significant details are published, but researchers either do not have full confidence in the root cause, " +
              "or do not have access to source code to confirm the result. Reasonable confidence exists, however, " +
              "that the bug is reproducible and at least one impact is able to be verified.",
          },
          unknown: {
            label: "Unknown",
            tooltip:
              "<strong>Unknown (U)</strong><br>" +
              "There are reports of impacts that indicate a vulnerability is present. " +
              "The reports indicate that the cause of the vulnerability is unknown, " +
              "or reports may differ on the cause or impacts of the vulnerability. ",
          },
        },
        tooltip:
          "<strong><big>Report Confidence (RC)</big></strong><br>" +
          "Measures the degree of confidence in the existence of the vulnerability " +
          "and the credibility of the known technical details. Sometimes, " +
          "only the existence of vulnerabilities is publicized, but without specific details. ",
      },
      severityScope: {
        label: "Scope",
        options: {
          changed: {
            label: "Changed",
            tooltip:
              "<strong>Changed (C)</strong><br>" +
              "An exploited vulnerability can affect resources beyond the security scope " +
              "managed by the security authority of the vulnerable component. In this case, " +
              "the vulnerable component and the impacted component are different and managed by different security authorities.",
          },
          unchanged: {
            label: "Unchanged",
            tooltip:
              "<strong>Unchanged (U)</strong><br>" +
              "An exploited vulnerability can only affect resources managed by the same security authority. In this case, " +
              "the vulnerable component and the impacted component are either the same, " +
              "or both are managed by the same security authority.",
          },
        },
        tooltip:
          "<strong><big>Scope (S)</big></strong><br>" +
          "The Scope metric captures whether a vulnerability in one vulnerable component " +
          "impacts resources in components beyond its security scope. ",
      },
      solve: "Mark as solved",
      tabTitle: "Severity",
      tooltip: "Assigned score according to CVSS 3.1 metrics",
      update: "Update",
      userInteraction: {
        label: "User Interaction",
        options: {
          none: {
            label: "None",
            tooltip:
              "<strong>None (N)</strong><br>" +
              "The vulnerable system can be exploited without interaction from any user.",
          },
          required: {
            label: "Required",
            tooltip:
              "<strong>Required (R)</strong><br>" +
              "Successful exploitation of this vulnerability requires a user to take some action before the vulnerability can be exploited. " +
              "For example, a successful exploit may only be possible during the installation of an application by a system administrator.",
          },
        },
        tooltip:
          "<strong><big>User Interaction (UI)</big></strong><br>" +
          "This metric determines whether the vulnerability can be exploited solely at the will of the attacker, " +
          "or whether a separate user (or user-initiated process) must participate in some manner.",
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
      onHold: "On Hold",
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
        closingDate: "Closing date",
        currentTreatment: "Current",
        cycles: "Cycles",
        dateTooltip: "Filter vulnerabilities based on the report date",
        efficacy: "Efficiency",
        info: "General details",
        lastReattackDate: "Last reattack date",
        lastRequestedReattackDate: "Last request",
        location: "Location",
        more: "...",
        reattack: "Reattack",
        reattacks: "Reattacks",
        reattacksTooltip:
          "Filter vulnerabilities based on the status of their reattack requests",
        reportDate: "Report date",
        requester: "Requester",
        specific: "Specific",
        specificType: {
          app: "Input",
          code: "LoC",
          infra: "Port",
        },
        status: "Status: ",
        tags: "Tags",
        treatment: "Treatment",
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
        where: "Locations",
      },
      vulnerabilityInfo: "vulnerability",
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
  table: {
    allOptions: "--All options--",
    clearFilters: "Clear Filters",
    filters: "Filters",
    noDataIndication: "There is no data to display",
    results: "Showing {{matches}} matching results out of {{total}}",
    search: "Search",
    tooltip: "Search filters for the table",
  },
  tagIndicator: {
    acceptedVulnerabilitiesBySeverity: "Accepted vulnerabilities by severity",
    acceptedVulnerabilitiesByUser: "Accepted vulnerabilities by user",
    findingsGroup: "Types of Vulnerabilities by Group",
    meanRemediate: "Mean (average) days to remediate",
    openFindingsGroup: "Open Types of Vulnerabilities by Group",
    openVulnsGroups: "Open vulnerabilities by group",
    remediatedAcceptedVuln:
      "How many vulnerabilities are remediated and accepted?",
    remediatedVuln: "How many vulnerabilities are remediated (closed)?",
    topOldestFindings: "Top Oldest Types of Vulnerabilities",
    undefinedTitle: "Undefined Treatment by Group",
    vulnerabilitiesByLevel: "Vulnerabilities by level",
    vulnerabilitiesByTag: "Vulnerabilities by tag",
    vulnerabilitiesByTreatments:
      "Vulnerabilities by Number of Treatment Changes",
    vulnerabilitiesByType: "Vulnerabilities by source",
    vulnsGroups: "Vulnerabilities by group",
  },
  taskContainer: {
    filters: {
      dateRange: {
        placeholder: "Report date (Range)",
      },
      groupName: {
        placeholder: "Group Name",
        tooltip: "Filter vulnerabilities based on group name",
      },
      treatment: {
        placeholder: "Treatment",
      },
      treatmentAcceptance: {
        placeholder: "Treatment Acceptance",
      },
    },
  },
  tours: {
    addGitRoot: {
      addButton: "Let's set up your repositories so we can analyze your code",
      proceedButton:
        "Great! Press the button to start cloning and analyzing your code",
      rootBranch: "Fill the branch of the code repository to analyze",
      rootCredentials:
        "Fill the credentials that will be used to clone the repository",
      rootEnvironment: "Name the type of environment that the code refers to",
      rootHasHealthcheck:
        "For currently on-going repositories, decide if we are going to analyze the existing code or only the new work from this point forward",
      rootUrl: "Fill the url of the code repository to analyze",
    },
    addGroup: {
      addButton:
        'Let us guide you through the process of setting up your project. That way we can start analyzing your code and report all the vulnerabilities we find. Press "New Group" to get started!',
      groupDescription:
        "Please add a description that will help you know which group is associated with which of your projects",
      groupName:
        "This is the name that will identify your project. It's automatically generated by us, so there's no need for you to rack your brain about names ;)",
      proceedButton: "Great! Press the button to create your new group.",
    },
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
  upgrade: {
    close: "Close",
    link: "Squad subscriptions",
    select: "Select the groups you would like to upgrade",
    success: {
      text: "You'll receive an email shortly",
      title: "Upgrade requested successfully",
    },
    text: "This functionality is only available for",
    title: "Subscription upgrade",
    unauthorized: "Contact your manager to request an upgrade",
    upgrade: "Upgrade",
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
      architect: "Architect",
      customerManager: "Customer Manager",
      executive: "Executive",
      hacker: "Hacker",
      reattacker: "Reattacker",
      resourcer: "Resourcer",
      reviewer: "Reviewer",
      user: "User",
      userManager: "User Manager",
      vulnerabilityManager: "Vulnerability Manager",
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
    duplicateSecret: "This secret has been already defined",
    email: "The email format is not valid",
    excludeFormat: "Root name should not be included in the exception pattern",
    excludePathHost: "The path should not include the host",
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
    integer: "This field can only contain an integer",
    invalidChar:
      "Invalid characters, use: alphanumerics, spaces and punctuations",
    invalidCommentParent: "The comment parent is invalid",
    invalidEmailInField: "The email address inserted is not valid",
    invalidEnvironmentUrl: "The environment URL is invalid",
    invalidFieldLength: "The value inserted in one of the fields is too large",
    invalidMarkdown: "Invalid or malformed markdown",
    invalidPhoneNumber: "The phone number is invalid",
    invalidSshFormat: "Invalid or malformed SSH private key",
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
    requestedTooSoon:
      "Please wait a minute before resending an invitation to this user",
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
    zeroOrPositive: "The number must be either 0 or positive",
  },
  verifyDialog: {
    fields: {
      verificationCode: "Verification code",
    },
    title: "Two-step verification",
    tour: {
      addMobile: {
        profile:
          "Add your mobile to send you verification codes. The mobile can be managed through the user information dropdown menu.",
      },
    },
    verify: "Verify",
  },
};

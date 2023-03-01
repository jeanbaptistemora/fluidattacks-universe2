import type { ResourceKey } from "i18next";

export const enTranslations: ResourceKey = {
  analytics: {
    barChart: {
      eventualities: "Unsolved events by group",
      exposureBenchmarkingCvssf: "Exposure benchmark",
      exposureByGroups: "Exposure by group",
      exposureTrendsByCategories: "Exposure trends by vulnerability category",
      meanTimeToRemediate: {
        tooltip: {
          alt: {
            default: "Mean time to remediate",
            nonTreated: "Non treated mean time to remediate",
            nonTreatedCvssf: "Non treated mean time to remediate & exposure",
          },
          default: "Mean time to remediate & exposure",
        },
      },
      mttrBenchmarking: {
        title: "Mean time to remediate (MTTR) benchmark",
        tooltip: {
          all: "Days per Exposure for all vulnerabilities",
          nonTreated: "Days per Exposure for non treated vulnerabilities",
        },
      },
      topVulnerabilities: {
        altTitle: {
          app: "App Exposure by type",
          code: "Code Exposure by type",
          infra: "Infra Exposure by type",
          vulnerabilities: "Vulnerabilities by type",
        },
        title: "Exposure by type",
        tooltip: {
          app: "Source of exposure of type App",
          code: "Source of exposure of type Code",
          cvssf: "Exposure",
          infra: "Source of exposure of type Infra",
          vulnerabilities: "Vulnerabilities",
        },
      },
      touchedFiles: {
        title: "Files with open vulnerabilities in the last 20 weeks",
      },
    },
    buttonToolbar: {
      download: {
        tooltip: "Download the chart as a .html file",
      },
      expand: {
        id: "expand_button_tooltip",
        tooltip: "View the chart in a pop-up window",
      },
      fileCsv: {
        tooltip: "Download the chart as a .csv file",
      },
      filter: {
        id: "filter_button_tooltip",
        tooltip: "Limit information to the selected variable",
      },
      information: {
        id: "information_button_tooltip",
        tooltip: "Go to information about the chart",
      },
      refresh: {
        id: "refresh_button_tooltip",
        tooltip: "Reload the default chart",
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
      oneHundredEighty: {
        text: "180",
        tooltip: "Data filtered from the last 180 days",
      },
      sixtyDays: {
        text: "60",
        tooltip: "Data filtered from the last 60 days",
      },
      thirtyDays: {
        text: "30",
        tooltip: "Data filtered from the last 30 days",
      },
    },
    pieChart: {
      availability: {
        title: "Group availability",
      },
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
        vulnerabilitiesUrl: {
          error:
            "No export currently available, please wait until the report is " +
            "finished before requesting a new file for this organization",
          text: "Vulnerabilities",
          tooltip: "Download csv file with all organization vulnerabilities",
        },
      },
      forces: {
        title: "Agent",
      },
    },
    stackedBarChart: {
      assignedVulnerabilities: {
        altTitle: "Vulnerabilities by assignee",
        title: "Exposure by assignee",
        tooltip: {
          cvssf: "Exposure",
          vulnerabilities: "Vulnerabilities",
        },
      },
      cvssfBenchmarking: {
        title: "Remediation rate benchmark",
      },
      distributionOverTimeCvssf: {
        altTitle: "Vulnerabilities management over time (%)",
        title: "Exposure management over time (%)",
        tooltip: {
          cvssf: "Exposure",
          vulnerabilities: "Vulnerabilities",
        },
      },
      exposedOverTimeCvssf: {
        title: "Exposure over time",
      },
      riskOverTime: {
        altTitle: "Vulnerabilities management over time",
        title: "Exposure management over time",
        tooltip: {
          cvssf: "Exposure",
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
      meanTimeToReattack: {
        title: "Mean time to request reattacks",
      },
      openVulnerabilities: {
        title: "Open vulnerabilities",
      },
      remediationCreated: {
        title: "Sprint exposure increment",
      },
      remediationRate: {
        title: "Remediation rate",
      },
      remediationRemediated: {
        title: "Sprint exposure change overall",
      },
      remediationSolved: {
        title: "Sprint exposure decrement",
      },
      totalTypes: {
        title: "Total types",
      },
      totalVulnerabilities: {
        title: "Total vulnerabilities",
      },
      vulnsWithUndefinedTreatment: {
        title: "Vulnerabilities with no treatment",
      },
    },
  },
  app: {
    errorPage:
      "Oops... something went wrong, if this keeps appearing feel free to submit a report through our ticket system",
    minimumWidth: "ARM is only available on desktops",
  },
  autoenrollment: {
    aboutToStart:
      "And that's it. You're about to start finding vulnerabilities.",
    acceptTerms: "By signing up, you agree with Fluid Attacks'",
    addRepository: "Add a code repository we can start hacking",
    alreadyInTrial: "Oops! It seems like you've already enjoyed a free trial.",
    and: "and",
    branch: {
      label: "Branch",
      placeholder: "qa",
    },
    canAddMore: "This is the first repo. You can add more when you finish!",
    cancelModal: {
      body: "Do you want to cancel your free trial?",
      no: "No",
      yes: "Yes",
    },
    corporateOnly:
      "To enjoy your free trial, sign up with a Corporate Email Account.",
    credentials: {
      auth: {
        azureToken: "Azure DevOps PAT",
        token: "Access Token",
        user: "User and Password",
      },
      azureOrganization: {
        text: "Azure Organization",
        tooltip:
          "The name of the azure organization related to the personal access token",
      },
      name: {
        label: "Credential name",
        placeholder: "Word/phrase identifier",
      },
      password: "Password",
      sshKey: "Private SSH Key",
      token: "Token",
      type: {
        https: "HTTPS",
        label: "Credential type",
        ssh: "SSH",
      },
      user: "User",
    },
    environment: {
      label: "Environment kind",
      placeholder: "qa",
      tooltip: "Description of the application environment",
    },
    exclusions: {
      label: "Exclusions ",
      placeholder: "/path_to_exclude",
      tooltip: "Insert up to five code exclusion paths",
    },
    groupDescription: {
      label: "Description of the group",
      placeholder: "Group description",
    },
    groupName: {
      label: "Group name ",
      placeholder: "My group name",
      tooltip: "Name that will be assigned to your new group",
    },
    languages: {
      checkLanguages: "Please check the supported languages for ",
      contactSales: {
        accept: "I accept the ",
        and: "and",
        confirmDescription:
          "Soon a member of our sales team will contact " +
          "you to show you all the benefits of the Continuous Hacking ",
        confirmSubtitle: "Your data was sent successfully.",
        description:
          "We'd love to chat with you. Please complete the following fields:",
        privacyPolicy: "Privacy policy",
        termsOfUse: "Terms of use",
        title: "Contact sales to get Squad Plan",
      },
      machineLanguages: {
        button: "Continue free trial registration",
        buttonSquadLanguages: "Don't see the language you're looking for? ",
        checkSquadLanguages: "Check Squad plan",
        description:
          "Discover deterministic vulnerabilities quickly through automated tools.",
        machinePlan: "Machine Plan",
        tag: "Free Trial",
        title: "Supported languages",
      },
      sidepanelButton: "Machine Plan",
      squadLanguages: {
        button: "Contact sales for Squad Plan",
        description:
          "Squad Plan expands the benefits of the Machine plan " +
          "and adds the skills of our expert talent (Manual Pentesting). " +
          "Contact our sales team if you need discover more complex and severe vulnerabilities.",
        description2: "All machine plan supported languages and :",
        squadPlan: "Squad Plan",
        squadSupportedCICD: "Supported CI/CDs",
        squadSupportedInfra: "Infrastructure",
      },
    },
    messages: {
      error: {
        enrollment: "Invalid enrollment data or user already exists",
        enrollmentUser: "Enrollment user already exists",
        group: "Invalid or used Group Name, please change your input",
        organization:
          "Invalid or used Organization Name, please change your input",
        repository: "Invalid repository information, please check again",
      },
      success: {
        body: "You started Machine Plan free trial",
        title: "Done!",
      },
    },
    next: "Next",
    notElegible:
      "You're not elegible for the free trial.\n" +
      "You have been an active user",
    organizationCountry: {
      label: "Organization country",
      tooltip: "Country where the organization is based",
    },
    organizationName: {
      label: "Organization name ",
      placeholder: "My organization",
      tooltip: "Name that will be assigned to your new organization",
    },
    privacyPolicy: "Privacy policy",
    proceed: "Start Free Trial",
    reportLanguage: "Report language ",
    reportLanguageTip:
      "Select the language of your preference to report vulnerabilities",
    setupOrganization: "Name your organization and group",
    step1: "Step 1 of 2",
    step2: "Step 2 of 2",
    subtitle: "To begin, add the first code repository",
    termsOfService: "Terms of service",
    title: "Let's create your group",
    url: {
      label: "Repository URL",
      placeholder: "https://gitrepository.yourproject/sms/...",
      tooltip:
        "Repository or fork. Examples:\n" +
        "https://example.com/user/repo.git\n" +
        "git@github.com:user/repo.git",
    },
    welcome: {
      modal: {
        button: "Go to the ARM platform",
        subtitle:
          "You will receive a notification by email " +
          "when we find the first vulnerability. in the meantime, " +
          "explore the ARM platform and learn about its main features",
        title:
          "Welcome to the Attack Resistance Management (ARM) platform: " +
          "We are now scanning your application!",
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
  components: {
    modal: {
      cancel: "Cancel",
      confirm: "Confirm",
    },
    navBar: {
      help: "Help",
      news: "News",
      toDo: "To-do",
    },
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
    errorText: "An error occurred with your configuration",
    title: "Configuration",
  },
  deleteVulns: {
    closedVuln: "A closed vulnerability cannot be removed",
    notSuccess: "Vulnerability could not be eliminated",
    reportingError: "Error while reporting",
    title: "Delete vulnerability",
  },
  forms: {
    closing: "Closure",
    events: "Events",
    findings: "Findings",
    progress: "Progress",
  },
  group: {
    accessDenied: {
      btn: "Update group",
      contact: "contact our team",
      moreInfo: "for\nmore information.",
      text: "Your group is suspended. Please add a\npayment method or",
      title: "Access denied",
    },
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
        unregistered: "Unregistered",
      },
      repository: "Repository",
      sendInvitation: "Invite",
      tableAdvice:
        "Below you'll find the authors that have contributed " +
        "to your group in the selected month, and one example commit",
      tooltip: {
        text: "Send group invitation to unregistered author",
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
      error: {
        hasDraftsRejected: "You have pending rejected drafts to review",
      },
      errorSubmit: "Please provide {{missingFields}} before submitting",
      hint: {
        description: "Hint: Description",
        empty: "Not available",
      },
      new: "New Finding",
      reject: {
        consistency: "Consistency",
        evidence: "Evidence",
        naming: "Naming",
        omission: "Omission",
        other: "Other",
        otherReason: "Why?",
        reason: "Reason",
        scoring: "Scoring",
        text: "Reject",
        title: "Reject Draft",
        tooltip: "Reject the submitted draft",
        writing: "Writing",
      },
      submit: {
        text: "Submit",
        tooltip: "Submit the draft for review",
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
        alerts: {
          editEvent: {
            eventNotFound: "The event has not been found",
            nonSolvedEvent: "The event has not been solved",
            success: "Event description has been updated",
          },
          rejectSolution: {
            nonRequestedVerification:
              "The event verification has not been requested",
            success: "Event solution has been rejected",
          },
        },
        cancel: "Cancel",
        edit: { text: "Edit", tooltip: "Modify the fields of the event" },
        markAsSolved: "Mark as solved",
        rejectSolution: {
          button: {
            text: "Reject solution",
            tooltip: "Reject the event solution",
          },
          modal: {
            observations: "What observations do you have?",
            title: "Observations",
          },
        },
        save: { text: "Save", tooltip: "Save changes" },
        solved: {
          date: "Resolution date",
          holds:
            "{{ length }} reattack(s) put on hold by this Event " +
            "will be set to Requested",
        },
      },
      eventBar: {
        message:
          "{{ vulnGroups }} groups FAILED: {{ openEvents }} event(s) " +
          "need actions since {{ timeInDays }} days ago.",
        tooltip: "You have unsolved events in {{ groups }}",
      },
      evidence: {
        alerts: {
          update: {
            success: "Evidence has been updated",
          },
        },
        edit: "Edit",
        editTooltip: "Modify the evidence for this event",
        noData: "There are no evidences",
      },
      form: {
        affectedReattacks: {
          alreadyClosed:
            "At least one of the selected reattacks was closed already",
          alreadyOnHold:
            "At least one of the selected reattacks was put on hold already",
          btn: {
            text: "Update Affected Reattacks",
            tooltip: "Put reattacks on hold on already existing Events",
          },
          description: "Please select the affected reattacks",
          eventSection: "Event",
          holdsCreate: "Reattack holds requested successfully",
          no: "No",
          sectionTitle: "Affected Reattacks",
          selection: "Please select the reattacks that would be affected",
          switchLabel:
            "Does this event have an impact on any ongoing reattacks?",
          title: "Update Affected Reattacks",
          yes: "Yes",
        },
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
        evidence: "Evidence images",
        evidenceFile: "Evidence file",
        invalidFileName: "Evidence filename must not have invalid chars",
        none: "None",
        other: "Other",
        responsible: "Person in charge (client)",
        root: "Root",
        rootPlaceholder: "Search by nickname...",
        type: "Type",
        wrongFileType: "Evidence files must have .pdf, .zip or .csv extension",
        wrongImageName:
          "Evidence name must have the following format " +
          "organizationName-groupName-10 alphanumeric chars.extension",
        wrongImageType:
          "Evidence images must have .png/.webm extension for animation" +
          "/exploitation and .png for evidences",
      },
      new: "New Event",
      remediationModal: {
        btn: {
          text: "Request verification",
          tooltip: "Request the verification for an event that has been solved",
        },
        justification: "Which was the applied solution?",
        titleRequest: "Justification",
      },
      selectedError: "There were selected events that do not apply",
      successCreate: "Event created successfully",
      successRequestVerification:
        "Verification has been requested successfully",
      titleSuccess: "Success",
      type: {
        authorizationSpecialAttack: "Authorization for a special attack",
        clientCancelsProjectMilestone: "The client cancels a project milestone",
        clientSuspendsProject: "The client explicitly suspends the project",
        cloningIssues: "Cloning issues",
        credentialsIssues: "Credentials issues",
        dataUpdateRequired: "Request user modification/workflow update",
        environmentIssues: "Environment issues",
        installerIssues: "Installer issues",
        missingSupplies: "Missing supplies",
        networkAccessIssues: "Network access issues",
        other: "Other",
        remoteAccessIssues: "Remote access issues",
        title: "Type",
        toeDiffersApproved: "ToE different than agreed upon",
        vpnIssues: "VPN issues",
      },
    },
    findings: {
      addModal: {
        alerts: {
          addedFinding: "The vulnerability has been added",
        },
        fields: {
          description: {
            label: "Description",
            tooltip: "Brief explanation of the vulnerability and how it works",
          },
          recommendation: {
            label: "Recommendation",
            tooltip: "General suggestion to solve the vulnerability",
          },
          title: { label: "Title", tooltip: "Vulnerability number and name" },
        },
        hint: {
          description: "Hint: Description",
          empty: "Not available",
        },
        title: "Add vulnerability",
      },
      boolean: {
        False: "No",
        True: "Yes",
      },
      buttons: {
        add: {
          text: "Add",
          tooltip: "Add vulnerability",
        },
        delete: {
          text: "Delete",
          tooltip: "Delete all about this vulnerability",
        },
        report: {
          text: "Generate report",
          tooltip:
            "Generate a report of vulnerabilities and send it to your email",
        },
      },
      closingPercentage: "Remediation %",
      deleteModal: {
        alerts: {
          vulnerabilitiesDeleted: "Vulnerabilities were deleted",
        },
        justification: {
          duplicated: "It is duplicated",
          falsePositive: "It is a false positive",
          label: "Justification",
          notRequired: "Vulnerability not required",
        },
        title: "Delete vulnerability",
      },
      description: {
        exploitable: "Exploitable:",
        firstSeen: "First seen:",
        lastReport: "Last report:",
        onHold: "On hold:",
        reattack: "Pending reattack:",
        requested: "Requested:",
        showLess: "Show less...",
        showMore: "Show more...",
        title: "Description",
        value: "{{count}} day ago",
        // eslint-disable-next-line camelcase -- It is required for react-i18next
        value_plural: "{{count}} days ago",
        verified: "Verified:",
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
        assigned: "Filter vulnerabilities based on who is the assigned",
        lastReport: "Filter by last report",
        reattack: "Filter by reattack",
        releaseDate: "Filter by Release Date",
        severity: "Filter by severity",
        status: "Filter by status",
        tags: "Filter by Tags",
        treatment: "Filter by Treatment",
        type: "Filter by type",
        where:
          "Filter by text on vulnerability locations (open locations column to load data)",
      },
      headersTooltips: {
        age: "Number of days elapsed since the vulnerability type was opened",
        closingPercentage:
          "Percentage of closed vulnerabilities, 100% if it was solved",
        lastReport: "Number of days since the last vulnerability was added",
        locations: "Number of instances of the vulnerability",
        reattack: "Current reattack status",
        severity: "Risk scoring according to CVSS 3.1",
        source: "Type of exposure source",
        status:
          "Current state of the vulnerability: Vulnerable if the vulnerabilty " +
          "persists, Safe if it was solved",
        treatment: "Current treatment status",
        type: "Vulnerability title",
        where: "Exact location of the vulnerability.",
      },
      reattack: {
        False: "-",
        True: "Pending",
      },
      records: {
        noData: "There are no records",
      },
      report: {
        age: {
          text: "Age",
          tooltip: "Filter type with age less than value",
        },
        alerts: {
          invalidVerificationCode: "The verification code is invalid",
          nonVerifiedStakeholder: "Try again in a few minutes",
        },
        cert: "  Certificate",
        certTooltip:
          "Receive a security testing certification with the up-to-date" +
          " Finding remediation data of this group. Before requesting it," +
          " make sure to fill out the Information section of Scope." +
          " (Available with Machine or Squad only)",
        closingDate: {
          text: "Closing date",
          tooltip:
            "Filter vulnerabilities based on closing date." +
            " Before the specified date",
        },
        data: "  Export",
        dataTooltip:
          "Receive a zip file containing the exported data of all the findings " +
          "of this group",
        filterReportDescription:
          "Here you can customize the length of the report " +
          "by selecting these fields",
        findingTitle: {
          text: "Type",
          tooltip: "Filter by type",
        },
        generateXls: "Generate XLS",
        lastReport: {
          text: "Last Report",
          tooltip: "Filter types by days since the last reported vulnerability",
        },
        location: {
          text: "Locations",
          tooltip: "Filter by location",
        },
        maxReleaseDate: {
          text: "Max release date",
          tooltip:
            "Filter out vulnerabilities with release date greater than value",
        },
        maxSeverity: {
          text: "Max severity",
          tooltip: "Filter out vulnerabilities with severity more than value",
        },
        minReleaseDate: {
          text: "Min release date",
          tooltip:
            "Filter out vulnerabilities with release date less than value",
        },
        minSeverity: {
          text: "Min severity",
          tooltip: "Filter out vulnerabilities with severity less than value",
        },
        modalClose: "Close",
        modalTitle: "Reports",
        pdf: "Executive",
        pdfTooltip:
          "Receive a pdf file with an executive report that gives you summarized information " +
          "about all the findings of this group",
        reattack: {
          // eslint-disable-next-line camelcase
          on_hold: "On hold",
          requested: "Requested",
          title: "Reattack",
          verified: "Verified",
        },
        state: "Status",
        treatment: "Treatment",
        verificationAlreadyRequested: "The verification has been requested",
        xls: "  Technical",
      },
      tableSet: {
        btn: {
          text: "Columns",
          tooltip: "Choose the fields you want to display",
        },
        modalTitle: "Edit columns",
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
          text: "Execution log",
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
      alreadyQueued:
        "There is already a Machine execution queued with the same parameters",
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
        // eslint-disable-next-line camelcase -- It is required for react-i18next
        add_plural: "Add new roots",
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
            verboseLabel: "Reason for editing/removing URLs",
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
        // eslint-disable-next-line camelcase -- It is required for react-i18next
        edit_plural: "Edit roots",
        errors: {
          duplicateNickname:
            "An active root with the same Nickname already exists please type a new nickname",
          duplicateUrl:
            "A root with the same URL/branch already exists in this organization. Please activate the exiting root.",
          duplicateUrlInTargetGroup:
            "A root with the same URL/branch already exists in the target group. Please activate the exiting root.",
          fileNotFound: "The file has not been found",
          hasVulns:
            "Can't update as there are already vulnerabilities reported for this root",
        },
        lastCloningStatusUpdate: "Last status update",
        lastStateStatusUpdate: "Last state update",
        state: "State",
      },
      git: {
        addEnvUrl: "Add Environment Url",
        addEnvironment: {
          apk: "Mobile App file",
          aws: "AWS account ID",
          success: "Environment added successfully",
          successTittle: "Added environment",
          type: "Environment Url Type",
          url: "Environment Url",
        },
        confirmBranch: "Make sure the new branch is equivalent to the old one",
        createdAt: "Creation date:",
        createdBy: "Created by:",
        envUrl: "Environment URL",
        envUrlType: "URL Type",
        envUrls: "Environment URLs",
        errors: {
          invalid: "Repository URL or branch are not valid",
          invalidBranch: "The branch was not found in the repository",
          invalidGitCredentials:
            "Git repository was not accessible with the given URL and credentials",
          rootInGitignore:
            "Root name should not be included in gitignore pattern",
          trial: "You can only have one root during the free trial",
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
          accept: "I accept the additional costs derived from the Health Check",
          confirm: "Would you like a Health Check for the existing code?",
          no: "No",
          rejectA:
            "I accept that Fluid Attacks will not include a revision of the existing code in the repository",
          rejectB:
            "I accept that the existing code contains vulnerabilities that will not be detected",
          rejectC:
            "I accept that the previously defined SLAs do not apply to this repository",
          tableHeader: "HCK",
          title: "Health Check",
          titleTooltip: "Health Check include for existing code",
          yes: "Yes",
        },
        manageEnvs: "Manage environments",
        manageEnvsTooltip:
          "Add, edit or remove environment URLs for the selected git root",
        removeEnvironment: {
          success: "Environment Url was removed successfully",
          successTitle: "Removed environment",
          title: "Remove Environment Url",
        },
        repo: {
          branch: "Branch",
          cloning: {
            message: "Message",
            status: "Status",
            sync: "Sync",
          },
          credentials: {
            azureOrganization: {
              text: "Azure Organization",
              tooltip:
                "The name of the azure organization related to the personal access token",
            },
            azureToken: "Azure DevOps PAT",
            checkAccess: {
              noAccess: "Credentials are invalid",
              success: "Success - Access checked!",
              text: "Check Access",
            },
            https: "HTTPS",
            name: "Credential Name",
            nameHint: "Repository SSH Key",
            oauth: "OAUTH",
            password: "Repository password",
            secrets: {
              add: "Add secret",
              description: "Secret description",
              key: "Key",
              remove: "Remove secret",
              removed: "Removed secret",
              success: "Added secret",
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
            userHttps: "User and Password",
          },
          environment: "Environment kind",
          environmentHint: "(production, qa or other)",
          headers: {
            createdAt: "Repo Creation Date",
            createdBy: "Added by (mail)",
            lastEditedAt: "Date last edited",
            lastEditedBy: "Last edited by (mail)",
          },
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
        title: "IP Roots",
      },
      url: {
        errors: {
          invalid: "Invalid URL",
          invalidCharacters: "Invalid URL characters",
        },
        host: "Host",
        modal: {
          title: "URL Root",
        },
        nickname: "Nickname",
        path: "Path",
        port: "Port",
        protocol: "Protocol",
        query: "Query",
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
        tooltip: {
          default: "Keep track of the status of all the approved findings.",
          openVulns:
            "Keep track of the status of all the approved findings.<br />Open Vulnerabilities ({{value}}).",
        },
      },
      forces: {
        text: "DevSecOps",
        tooltip:
          "Check the details about all the executions of our DevSecOps " +
          "agent in your CI/CD pipeline",
      },
      indicators: {
        text: "Analytics",
        tooltip:
          "See charts and figure on the status and details of reported " +
          "vulnerabilities and your remediation practices",
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
      codeLanguages: {
        lang: "Language",
        loc: "Lines of Code",
        percent: "Percentage",
        title: "Code Languages",
      },
      inputs: {
        actionButtons: {
          addButton: {
            text: "Add",
            tooltip: "Add new input",
          },
          attackedButton: {
            text: "Attacked",
            tooltip: "Mark selected inputs as attacked",
          },
          cancelButton: {
            text: "Cancel",
            tooltip: "Cancel",
          },
          removeButton: {
            text: "Remove",
            tooltip: "Remove non-enumerated input",
          },
        },
        addModal: {
          alerts: {
            alreadyExists: "The input already exists.",
            invalidCharacter: "Field contains forbidden characters",
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
          title: "Add input",
        },
        alerts: {
          alreadyUpdate: "Something modified the input during the edition.",
          invalidAttackedAt:
            "The attacked at is not valid. There is a new datetime.",
          markAsAttacked: {
            success: "Input has been marked as attacked.",
          },
          nonPresent: "The input is not present.",
          updateInput: "Input has been updated.",
        },
        attackedAt: "Attacked at",
        attackedBy: "Attacked by",
        bePresent: "Be present",
        bePresentUntil: "Be present until",
        commit: "Commit",
        component: "Component",
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
          status: {
            placeholder: "Status",
            tooltip: "Filter by status",
          },
        },
        firstAttackAt: "First attack at",
        no: "No",
        remove: {
          alerts: {
            success: "Input has been removed.",
          },
        },
        root: "Root",
        safe: "Safe",
        seenAt: "Seen at",
        seenFirstTimeBy: "Seen first time by",
        status: "Status",
        vulnerable: "Vulnerable",
        yes: "Yes",
      },
      lines: {
        actionButtons: {
          addButton: {
            text: "Add",
            tooltip: "Add new lines",
          },
          editButton: {
            text: "Edit",
            tooltip: "Edit attacked lines",
          },
          verifyButton: {
            text: "Verified",
            tooltip: "Verify attacked file",
          },
        },
        addModal: {
          alerts: {
            alreadyExists: "The lines already exists.",
            success: "Lines has been added.",
          },
          close: "Close",
          fields: {
            filename: "Filename",
            lastAuthor: "Last author",
            lastCommit: "Last commit",
            loc: "Lines of code",
            modifiedDate: "Modified date",
            root: "Root",
          },
          title: "Add lines",
        },
        alerts: {
          verifyToeLines: {
            success: "Lines has been verified.",
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
            invalidAttackedLinesBetween:
              "The attacked lines must be between 0 and the loc.",
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
          status: {
            placeholder: "Status",
            tooltip: "Filter by status",
          },
        },
        firstAttackAt: "First attack at",
        formatters: {
          attackedLines: {
            tooltip: "Press enter to save",
          },
        },
        lastAuthor: "Last author",
        lastCommit: "Last commit",
        loc: "LOC",
        modifiedDate: "Modified date",
        no: "No",
        root: "Root",
        safe: "Safe",
        seenAt: "Seen at",
        sortsRiskLevel: "Priority (IA/ML)",
        sortsSuggestions: "Suggested Vulnerabilities",
        status: "Status",
        vulnerable: "Vulnerable",
        yes: "Yes",
      },
      ports: {
        actionButtons: {
          addButton: {
            text: "Add",
            tooltip: "Add new port",
          },
          attackedButton: {
            text: "Attacked",
            tooltip: "Mark selected ports as attacked",
          },
          cancelButton: {
            text: "Cancel",
            tooltip: "Cancel",
          },
        },
        addModal: {
          alerts: {
            alreadyExists: "The port already exists.",
            success: "Port has been added.",
          },
          close: "Close",
          fields: {
            IPRoot: "IP Root",
            port: "Port",
          },
          title: "Add port",
        },
        address: "Address",
        alerts: {
          alreadyUpdate: "Something modified the port during the edition.",
          markAsAttacked: {
            success: "Port has been marked as attacked.",
          },
          nonPresent: "The port is not present.",
          updatePort: "Port has been updated.",
        },
        attackedAt: "Attacked at",
        attackedBy: "Attacked by",
        bePresent: "Be present",
        bePresentUntil: "Be present until",
        commit: "Commit",
        filters: {
          address: {
            placeholder: "Address",
            tooltip: "Filter by address",
          },
          bePresent: {
            placeholder: "Be present (refetch)",
            tooltip: "Filter by be present",
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
          status: {
            placeholder: "Status",
            tooltip: "Filter by status",
          },
        },
        firstAttackAt: "First attack at",
        no: "No",
        port: "Port",
        root: "Root",
        safe: "Safe",
        seenAt: "Seen at",
        seenFirstTimeBy: "Seen first time by",
        status: "Status",
        vulnerable: "Vulnerable",
        yes: "Yes",
      },
      tabs: {
        inputs: {
          text: "Inputs",
          tooltip:
            "Track which application/infrastructure inputs have been reviewed",
        },
        languages: {
          text: "Languages",
          tooltip: "Track the language distribution inside your code",
        },
        lines: {
          text: "Lines",
          tooltip: "Track which source code lines have been reviewed",
        },
        ports: {
          text: "Ports",
          tooltip: "Track which ports have been reviewed",
        },
      },
    },
  },
  groupAlerts: {
    acceptanceApproved: "Indefinite acceptance has been approved",
    acceptanceRejected: "Indefinite acceptance has been rejected",
    accessDenied: "Access denied",
    confirmedVulnerabilitySuccess: "Vulnerability has been confirmed",
    confirmedZeroRiskSuccess: "Zero risk vulnerability has been confirmed",
    draftAlreadyApproved: "This finding has already been approved",
    draftAlreadySubmitted: "This finding has already been submitted",
    draftNotSubmitted:
      "This finding has not been submitted yet or it might've been rejected by someone else",
    draftWithoutVulns:
      "This finding can not been approved without vulnerabilities",
    errorApprove:
      "This finding can not been approved without {{missingFields}}",
    errorNetwork: "Check your network connection",
    errorTextsad: "There is an error :(",
    expectedPathToStartWithRepo:
      "Expected path to start with the repo nickname",
    expectedVulnToHaveNickname: "Expected vulnerability to have repo_nickname",
    expiredInvitation: "The stakeholder has an expired invitation",
    fileTypeCsv: "The file must have .csv extension",
    fileTypeEvidence: "The image must be .png, .webm type",
    fileTypePy: "The file must have .py or .exp extension",
    fileTypeWrong: "The file has an unknown or non-allowed format",
    fileTypeYaml: "The file must be .yaml or .yml type",
    fileUpdated: "File updated ;)",
    groupInfoUpdated: "Group information updated successfully",
    invalid: "is invalid",
    invalidAssigned: "Please select a valid assigned user",
    invalidCannotModifyNicknameWhenClosing:
      "Invalid, you cannot change the nickname while closing",
    invalidCommitHash: "Invalid commit hash",
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
        "by the defined policy",
      severityOutOfRange:
        "Finding severity outside of the acceptance range set by the defined policy",
    },
    pathValue: "Path value should not use backslash.",
    portValue: "Port value should be between 0 and 65535.",
    rangeError: "Range limits are wrong.",
    recordsRemoved: "Records have been removed successfully",
    rejectedVulnerabilitySuccess: "Vulnerability has been rejected",
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
    tooManyRequests:
      "Too many requests - Please wait 1 minute and make the request again",
    updated: "Updated",
    updatedTitle: "Correct!",
    value: "Value",
    verificationAlreadyRequested: "Verification already requested",
    verifiedSuccess: "The vulnerability was marked as verified",
    verifiedSuccessPlural: "The vulnerabilities were marked as verified",
    vulnClosed: "Vulnerability has already been closed",
    vulnerabilityIsNotSubmitted: "Vulnerability has not been submitted",
    zeroRiskAlreadyRequested: "Zero risk vulnerability already requested",
    zeroRiskAlreadyUploaded:
      "Uploaded vulnerability is a confirmed Zero Risk: {{info}}",
    zeroRiskIsNotRequested: "Zero risk vulnerability is not requested",
  },
  info: {
    commit: "Commit:",
    deploymentDate: "Deploy date:",
  },
  legalNotice: {
    accept: "Accept and continue",
    description: {
      legal:
        "ARM, Copyright (c) {{currentYear}} Fluid Attacks. This platform contains " +
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
        "By using the Fluid Attacks' Attack Resistance Management platform, you agree to our ",
      privacyLinkText: "Privacy Policy",
    },
    rememberCbo: {
      text: "Remember my decision",
      tooltip: "Mark the checkbox if you want this decision to be permanent",
    },
    title: "Legal notice",
  },
  login: {
    auth: "Sign in to Fluid Attacks' ARM Platform",
    bitbucket: "Continue with Bitbucket",
    generalData: {
      description:
        "Now enjoy the new section of ARM called Compliance. In this section, " +
        "you can visualize the percentage of compliance your organization and groups have " +
        "concerning different cybersecurity standards and you will be able to see how your " +
        "organization is positioned concerning other companies.",
      newFeature: "New Feature",
      privacy: "All the information will be securely saved as a per the",
      subtitle:
        "How am I in compliance with security standards as an organization?",
    },
    google: "Continue with Google",
    microsoft: "Continue with Microsoft",
    newuser: "If you are a new user, click below to sign up.",
    noEnrolledUser: {
      button: "Start free trial",
      subtitle1: "There is no ARM account for ",
      subtitle2: ". We recommend you start our free trial and ",
      subtitle3: "enjoy all Machine Plan benefits for 21 days.",
      title:
        "Looks like you're new to our Attack Resistance Management Platform.",
    },
    privacyLinkText: "Privacy Policy",
    termsOfUseLinkText: "Terms of Use",
  },
  navbar: {
    config: {
      text: "Configuration",
      tooltip: "Some additional configurations here",
    },
    credentials: "Credentials",
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
    },
    featurePreview: "Feature preview",
    help: {
      chat: "Live Chat",
      expert: "Talk to a hacker",
      extra: {
        chat: "Fast and personalized attention",
        expert: "Request any help you need through a scheduled videoconference",
        mail: "Direct communication channel through an email ticketing system",
      },
      options: {
        chat: {
          description: "Solve questions about using our ARM platform",
          title: "Live Chat",
        },
        docs: {
          description:
            "Read our product documentation and related help articles",
          title: "Documentation",
        },
        expert: {
          description:
            "Discuss any question or issue with reported vulnerabilities",
          title: "Talk to a hacker",
        },
        mail: {
          description:
            "Report any problem or request a new feature for the platform",
          title: "help@fluidattacks.com",
        },
      },
      support: "Support",
      tooltip: "For more information",
    },
    logout: "Log out",
    mobile: "Mobile",
    newsTooltip: "Latest updates about ARM",
    notification: "Notifications",
    role: "Role:",
    searchPlaceholder: "Search group",
    task: {
      text: "Todos",
      tooltip: {
        assigned: "To-Do List",
        assignedless: "You don't have any vulnerability assigned",
      },
    },
    token: "API token",
    user: "Add stakeholder",
  },
  organization: {
    tabs: {
      analytics: {
        text: "Analytics",
        tooltip: "Organization status at a glance",
      },
      billing: {
        authors: {
          headers: {
            activeGroups: "Active groups",
            authorEmail: "Author email",
            authorName: "Author name",
          },
          label:
            "Below you'll find the authors that have contributed " +
            "to your organization in the selected month.",
          title: "Authors",
        },
        groups: {
          headers: {
            costsTotal: "Total costs ($)",
            groupName: "Group name",
            managed: "Payment methods",
            numberAuthors: "Month-To-Date Authors",
            tier: "Tier",
          },
          managed: {
            managed: "Managed",
            notManaged: "Not managed",
            title: "Managed",
            tooltip: "If the payment method is managed",
            trial: "Trial",
            underReview: "Under review",
          },
          name: "Group name",
          paymentMethod: "Payment Method",
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
              invalidPaymentBusinessName:
                "Payment method business name must be match with group business name",
            },
            subscription: "Subscription",
            success: {
              body: "Group data successfully updated",
              title: "Success",
            },
            title: "Update Group",
            types: {
              free: "Free",
              machine: "Machine",
              squad: "Squad",
            },
          },
        },
        overview: {
          costsTotal: {
            content: "{{costsTotal}} $",
            info: "Month-To-Date total organization costs",
            title: "Total costs",
          },
          numberAuthorsMachine: {
            content: "{{numberAuthorsMachine}} Author(s)",
            info: "Month-To-Date Machine authors",
            title: "Machine authors",
          },
          numberAuthorsSquad: {
            content: "{{numberAuthorsSquad}} Author(s)",
            info: "Month-To-Date Squad authors",
            title: "Squad authors",
          },
          numberGroupsMachine: {
            content: "{{numberGroupsMachine}} Group(s)",
            info: "Number of Machine groups",
            title: "Machine groups",
          },
          numberGroupsSquad: {
            content: "{{numberGroupsSquad}} Group(s)",
            info: "Number of Squad groups",
            title: "Squad groups",
          },
          title: {
            info: "Billing information for {{organizationName}}",
            text: "Organization overview",
          },
        },
        paymentMethods: {
          add: {
            button: {
              label: "Add payment method",
              tooltip: "Add Credit cards or other payment methods",
            },
            creditCard: {
              add: "Add credit card",
              cvc: {
                label: "Card CVC",
                placeholder: "123",
              },
              default: "Make card default payment method",
              expirationMonth: {
                label: "Expiry month",
                placeholder: "MM",
              },
              expirationYear: {
                label: "Expiry year",
                placeholder: "YY",
              },
              label: "Credit card",
              number: {
                label: "Card number",
                placeholder: "1234 1234 1234 1234",
              },
              otherPaymentMethod: "Other payment methods",
            },
            errors: {
              alreadyExists:
                "Provided payment method already exists. Please update or delete it first",
              couldNotBeCreated:
                "Payment method could not be created. Please make sure all the details you provided are correct",
            },
            label: "Select payment method",
            otherMethods: {
              add: "Add other payment method",
              businessName: "Business name",
              city: "City",
              country: "Country",
              creditCard: "Credit card",
              email: "Email",
              label: "Other methods",
              rut: "Rut",
              state: "State",
              taxId: "TaxId",
            },
            success: {
              body: "Payment method successfully added",
              title: "Success",
            },
            title: "Add payment method",
          },
          defaultPaymentMethod: "(Default)",
          paymentType: {
            creditCard: "Credit card",
            otherMethod: "Other",
          },
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
            errors: {
              noPaymentMethod: "The payment method does not exist",
            },
            modal: {
              default: "Make card default payment method",
              expirationMonth: "Card expiration month",
              expirationYear: "Card expiration year",
              update: "Update payment method",
            },
            success: {
              body: "Payment method successfully updated",
              title: "Success",
            },
          },
        },
        portal: {
          title: "Invoices",
        },
        text: "Billing",
        tooltip: "Billing and subscriptions for your organization",
      },
      compliance: {
        tabs: {
          overview: {
            benchmark: {
              title: "Benchmark",
            },
            cards: {
              avgOrganization: "Avg organization",
              bestOrganization: "Best organization",
              days: "days",
              myOrganization: "My organization",
              worstOrganization: "Worst organization",
            },
            organizationCompliance: {
              complianceLevel: {
                info: "The organization has complied with the {{percentage}}% of the standards",
                title: "Compliance level of {{organizationName}}",
              },
              complianceWeeklyTrend: {
                info: "The organization has changed the compliance by {{percentage}}% in the last week",
                title: "Weekly trend",
              },
              etToFullCompliance: {
                info: "The estimated time to comply with all the standards is {{days}} days",
                title: "ET to full compliance",
              },
              title: {
                info: "Compliance information for {{organizationName}}",
                text: "Organization compliance",
              },
            },
            standardWithLowestCompliance: {
              complianceLevelOfStandard: {
                info: "The standard with the lowest compliance is {{standardTitle}} with {{percentage}}%",
                title: "Compliance level of standard",
              },
              title: {
                info: "The standard with lowest compliance within the organization",
                text: "Standard with lowest compliance",
              },
            },
            text: "Overview",
            tooltip: "Overview of the compliance with the standards",
          },
          standards: {
            alerts: {
              generatedReport:
                "The report has been generated (Allow the redirects to download the file)",
            },
            buttons: {
              generateReport: {
                text: "Generate report",
                tooltip:
                  "Download a report of the unfulfilled standards (Allow the redirects to download the file)",
              },
            },
            cards: {
              requirement: "Requirement",
              showAll: "Show all",
            },
            generateReportModal: {
              action: "Action",
              buttons: {
                generateReport: {
                  text: "Generate report",
                  tooltip:
                    "Download a report of the unfulfilled standards (Allow the redirects to download the file)",
                },
              },
              exclude: "Exclude",
              excludeAll: "Exclude all",
              include: "Include",
              includeAll: "Include all",
              title: "Generate report",
              unfulfilledStandard: "Unfulfilled standard",
            },
            text: "Standards",
            tooltip: "Compliance information for standards",
            unfulfilledStandards: {
              title: "Unfulfilled standards",
            },
          },
        },
        text: "Compliance",
        tooltip: "Compliance with the standards in your organization",
      },
      credentials: {
        actionButtons: {
          addButton: {
            text: "Add",
            tooltip: "Add organization credentials",
          },
          azureButton: {
            text: "Azure",
            tooltip: "Add Azure OAuth organization credentials",
          },
          bitbucketButton: {
            text: "Bitbucket",
            tooltip: "Add Bitbucket OAuth organization credentials",
          },
          editButton: {
            text: "Edit",
            tooltip: "Edit credentials of the organization",
          },
          githubButton: {
            text: "Github",
            tooltip: "Add GitHub OAuth organization credentials",
          },
          gitlabButton: {
            text: "Gitlab",
            tooltip: "Add GitLab OAuth organization credentials",
          },
          removeButton: {
            confirmMessage:
              "{{credentialName}} will be removed from the organization",
            confirmTitle: "Remove credentials?",
            text: "Remove",
            tooltip: "Remove credentials from the organization",
          },
        },
        alerts: {
          addSuccess: "Credentials has been added.",
          editSuccess: "Credentials has been edited.",
          removeSuccess: "Credentials has been removed.",
        },
        credentialsModal: {
          form: {
            add: "Add",
            auth: {
              azureToken: "Azure DevOps PAT",
              token: "Access Token",
              user: "User and Password",
            },
            azureOrganization: {
              text: "Azure Organization",
              tooltip:
                "The name of the azure organization related to the personal access token",
            },
            edit: "Edit",
            isPat: "Use as Azure DevOps PAT",
            name: {
              label: "Credential name",
              placeholder: "Test credential",
            },
            password: "Repository password",
            sshKey: "Private SSH Key",
            token: "Repository access token",
            type: {
              https: "HTTPS",
              label: "Credential type",
              ssh: "SSH",
            },
            user: "Repository user",
          },
        },
        table: {
          columns: {
            name: "Name",
            owner: "Owner",
            type: "Type",
          },
        },
        text: "Credentials",
        tooltip: "Credentials for your organization",
      },
      groups: {
        disabled: "Disabled",
        editGroup: {
          sprintStartDate: {
            text: "Start Date",
            tooltip: "The start date of Sprint for this product",
          },
        },
        enabled: "Enabled",
        filtersTooltips: {
          forces: "Filter by forces",
          groupName: "Filter by group name",
          machine: "Filter by machine",
          plan: "Filter by plan",
          service: "Filter by service",
          squad: "Filter by squad",
          subscription: "Filter by subscription",
          tier: "Filter by tier",
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
          invalidName: "Name specified for the group is not allowed",
          language: {
            EN: "English",
            ES: "Spanish",
            text: "Report language",
            tooltip: "Language in which findings should be reported",
          },
          machine: {
            text: "Include Machine Plan?",
            tooltip:
              "Machine Plan is for clients that want to discover deterministic " +
              "vulnerabilities quickly through automated tools",
          },
          managed: {
            managed: "Managed",
            notManaged: "Not managed",
            text: "Managed",
            tooltip: "Enable manually managed group",
            trial: "Trial",
            underReview: "Under review",
          },
          name: "Group name",
          new: {
            group: "New group",
            text: "New group",
            tooltip: "Create a new group",
          },
          oneshot: {
            text: "One-Shot Hacking",
            tooltip:
              "One-Shot Hacking searches for vulnerabilities in only " +
              "one specific version of your project",
          },
          organization: {
            text: "Organization",
            tooltip:
              "Name of the organization that is associated with this group",
          },
          service: {
            black: "Black-box",
            title: "Type of testing",
            white: "White-box",
          },
          sprintDuration: {
            text: "Sprint Length",
            tooltip:
              "The length of the average Sprint for this product in weeks",
          },
          squad: {
            text: "Include Squad Plan?",
            tooltip:
              "Squad Plan is for clients that want to discover more varied, " +
              "even more complex vulnerabilities through ethical hacking",
          },
          success: "Group created successfully",
          switch: {
            no: "No",
            yes: "Yes",
          },
          titleSuccess: "Success",
          trial: "You can only have one group during the free trial",
          type: {
            continuous: "Continuous Hacking",
            oneShot: "One-Shot Hacking",
            title: "Type of service",
            tooltip: "Type of subscription",
          },
        },
        overview: {
          coveredAuthors: {
            content: "{{coveredAuthors}}",
            info: "Number of authors of all repositories of the organization",
            title: "Covered authors",
          },
          coveredRepositories: {
            content: "{{coveredRepositories}}",
            info: "Number of repositories from all groups of the organization",
            title: "Covered repositories",
          },
          missedAuthors: {
            content: "{{missedAuthors}}",
            info: "Number of authors of repositories out of the scope",
            title: "Missed authors",
          },
          missedRepositories: {
            content: "{{missedRepositories}}",
            info: "Number of repositories out of the scope",
            title: "Missed repositories",
          },
          title: {
            info: "Scope information for {{organizationName}}",
            text: "Scope overview",
          },
        },
        plan: "Plan",
        role: "Role",
        status: {
          header: "Group status",
          managed: "Subscribed",
          notManaged: "Subscribed",
          trial: "Free-trial",
          trialDaysTip: "You have {{ remainingDays }} days left",
          trialTip: "You have active a Free-Trial subscription",
          underReview: "Suspended",
          underReviewTip:
            "This group has been suspended due to non-payment " +
            "or lack of payment setup",
        },
        text: "Groups",
        tooltip: "Groups that belong to the organization",
        vulnerabilities: {
          header: "Vulnerabilities",
          inProcess: "In process",
          open: "{{ openFindings }} types found",
        },
      },
      policies: {
        errors: {
          acceptanceSeverity:
            "Acceptance severity score must be a positive floating number between 0.0 and 10.0",
          acceptanceSeverityRange:
            "Minimum acceptance score should be lower than the maximum value",
          inactivityPeriod:
            "Inactivity period should be greater than the provided value",
          invalidBreakableSeverity:
            "The minimum breaking severity score must be a positive floating number between 0.0 and 10.0",
          maxAcceptanceDays:
            "Maximum acceptance days should be a positive integer between 0 and 180",
          maxNumberAcceptances:
            "Maximum number of acceptances should be a positive integer",
          vulnerabilityGracePeriod:
            "Maximum acceptance days should be a positive integer",
        },
        externalTooltip: "Go to information about policy",
        findings: {
          action: "Action",
          addPolicies: {
            success:
              "Remember that the application of the policy requires the approval of a user with manager role",
          },
          date: "Date",
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
            finding: "Vulnerability type",
            tags: "Tags",
          },
          handlePolicies: {
            success: {
              approved: "The policy will be applied within the next minutes",
              rejected: "The policy was successfully rejected",
            },
          },
          status: "Status",
          submitPolicies: {
            modalTitle: "Re-submit organization vulnerability policy",
          },
          tags: "Tags",
          title: "Permanent acceptance",
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
          type: "Vulnerability type",
        },
        group: {
          success: "Group policies updated successfully",
          tooltip:
            "Policies inheritance, you can override rules set up in the " +
            "organization for this group",
        },
        policies: {
          acceptanceSeverityRange:
            "Temporal acceptance: CVSS 3.1 score range allowed for assignment",
          inactivityPeriod:
            "Login inactivity: Number of days to remove a stakeholder " +
            "due to inactivity",
          maxAcceptanceDays:
            "Temporal acceptance: Maximum number of days for assignment",
          maxAcceptanceSeverity:
            "Temporal acceptance: Maximum CVSS 3.1 score allowed for assignment",
          maxNumberAcceptances:
            "Temporal acceptance: Maximum number of assignments for a single " +
            "vulnerability",
          minAcceptanceSeverity:
            "Temporal acceptance: Minimum CVSS 3.1 score allowed for assignment",
          minBreakingSeverity:
            "DevSecOps: Minimum CVSS 3.1 score of vulnerable spots " +
            "for the agent to break the build in Strict Mode",
          vulnerabilityGracePeriod:
            "DevSecOps: Days before agent starts breaking the build for new " +
            "vulnerabilities",
        },
        policy: "Policy",
        recommended: {
          acceptanceSeverityRange: "Recommended value: 0.0 - 0.0",
          inactivityPeriod: "Recommended value: 90 days",
          maxAcceptanceDays: "Recommended value: 0",
          maxAcceptanceSeverity: "Recommended value: 0.0",
          maxNumberAcceptances: "Recommended value: 0",
          minAcceptanceSeverity: "Recommended value: 0.0",
          minBreakingSeverity: "Recommended value: 0.0",
          vulnerabilityGracePeriod: "Recommended value: 0",
        },
        save: "Save",
        success: "Organization policies updated successfully",
        successTitle: "Success",
        text: "Policies",
        title: "Policies",
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
          disabled: "Please choose only one user to edit",
          success: "was successfully edited",
          text: "Edit",
          tooltip: "Edit user information",
        },
        modalAddTitle: "Add a new user to this organization",
        modalEditTitle: "Edit stakeholder information",
        removeButton: {
          confirmMessage: "will be removed from the organization",
          confirmTitle: "Remove stakeholder?",
          // eslint-disable-next-line camelcase -- It is required for react-i18next
          confirmTitle_plural: "Remove stakeholders?",
          success: "was successfully removed from the organization",
          successPlural:
            "Many users were successfully removed from the organization",
          text: "Remove",
          tooltip: "Remove stakeholder from the organization",
        },
        successTitle: "Success",
        text: "Stakeholders",
        tooltip: "Add and remove users from the organization",
      },
      weakest: {
        buttons: {
          add: {
            text: "Integrate",
            tooltip: "Integrate by adding PAT or OAuth credentials",
          },
          addRepositories: {
            text: "Add new roots",
            tooltip:
              "Add many roots with same branch, credential, env and health check",
          },
        },
        formatter: {
          plus: {
            tooltip: "Add new root using the URL",
          },
        },
        modal: {
          select: "In which group the root will be added",
          // eslint-disable-next-line camelcase -- It is required for react-i18next
          select_plural: "In which group the roots will be added",
          title: "Select group",
        },
        table: {
          action: "Action",
          lastCommitDate: "Last commit date",
          url: "Repository URL",
        },
        text: "Out of the scope",
        tooltip: "Repositories not included in ARM",
      },
    },
  },
  profile: {
    credentialsModal: {
      actionButtons: {
        addButton: {
          text: "Add",
          tooltip: "Add organization credentials",
        },
        editSecretsButton: {
          text: "Edit secrets",
          tooltip: "Edit multiple credentials secrets",
        },
      },
      alerts: {
        addSuccess: "Credentials has been added.",
        editSuccess: "Credentials has been edited.",
        removeSuccess: "Credentials has been removed.",
      },
      form: {
        add: "Add",
        edit: "Edit",
        https: "HTTPS",
        httpsType: {
          accessToken: "Access Token",
          userAndPassword: "User and Password",
        },
        name: {
          label: "Name",
          placeholder: "",
        },
        newSecrets: "New secrets",
        organization: "Organization",
        password: "Repository password",
        ssh: "SSH",
        sshKey: {
          label: "Private SSH Key",
          placeholder:
            "-----BEGIN OPENSSH PRIVATE KEY-----\n" +
            "SSH PRIVATE KEY...\n" +
            "-----END OPENSSH PRIVATE KEY-----",
        },
        token: "Repository access token",
        user: "Repository user",
      },
      formatters: {
        actions: {
          removeCredentials: {
            confirmModal: {
              message: "Credentials will be removed from all git roots",
              title: "Remove credentials",
            },
          },
        },
      },
      table: {
        columns: {
          action: "Action",
          id: "Id",
          name: "Name",
          organization: "Organization",
          type: "Type",
        },
      },
      title: "Credentials",
    },
    mobileModal: {
      add: "Add",
      alerts: {
        additionSuccess: "Mobile has been added.",
        editionSuccess: "Mobile has been updated.",
        invalidVerificationCode: "The verification code is invalid",
        nonSentVerificationCode:
          "Check your mobile number and retry in a minute",
        nonVerifiedStakeholder: "Try again in a few minutes",
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
    continue: "Continue",
    continueAsBtn: "Continue as",
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
      AGENT_TOKEN: {
        name: "DevSecOps agent token alert",
        tooltip:
          "Get notifications when a DevSecOps Agent token is generated or " +
          "reset.",
      },
      CHARTS_REPORT: {
        name: "Analytics report",
        tooltip:
          "Get charts and data on the status and characteristics " +
          "of reported vulnerabilities and your remediation practices.",
      },
      COMMENTS: "Consulting",
      EVENT_REPORT: {
        name: "Event alert",
        tooltip:
          "Get information about an event when it is reported in a group.",
      },
      FILE_UPDATE: {
        name: "Files updates",
        tooltip: "Get notifications when a file is added or removed.",
      },
      GROUP: "GROUP",
      GROUP_INFORMATION: {
        name: "Group information",
        tooltip:
          "Get a notification when the information of one of " +
          "your groups changes or a group is deleted.",
      },
      GROUP_REPORT: {
        name: "GROUP_REPORT",
        tooltip: "GROUP_REPORT",
      },
      NEW_COMMENT: {
        name: "Consulting",
        tooltip:
          "Get notifications when an ARM user submits a comment concerning " +
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
      PORTFOLIO_UPDATE: {
        name: "Portfolio updates",
        tooltip: "Get notifications when a portfolio is created or removed.",
      },
      REMEDIATE_FINDING: {
        name: "Vulnerability updates",
        tooltip:
          "Get notifications when a new vulnerability is discovered, " +
          "a vulnerability fix is reported " +
          "or a specific vulnerability is removed.",
      },
      REMINDER_NOTIFICATION: {
        name: "Inactivity alert",
        tooltip:
          "Get notifications when three weeks have passed " +
          "since you last used the platform.",
      },
      ROOT_UPDATE: {
        name: "Root updates",
        tooltip:
          "Get notifications on the status of root cloning, environment " +
          "adds, or deletes. Too when a user deactivates, adds, updates, or " +
          "moves a root to another group.",
      },
      SERVICE_UPDATE: {
        name: "Services updates",
        tooltip: "Get notifications when services are updated.",
      },
      UNSUBSCRIPTION_ALERT: {
        name: "Unsubscription alert",
        tooltip: "Get notifications when a user unsubscribes.",
      },
      UPDATED_TREATMENT: {
        name: "Treatment updates",
        tooltip:
          "Get notifications when a user defines how to address a " +
          "vulnerability, a permanent treatment is requested or approved, " +
          "and a temporal treatment is close to ending.",
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
          "The number of locations in your system that still have vulnerable status.",
      },
      riskExposure: {
        label: "Total Risk Exposure (CVSSF)",
        remediated: "Vulnerability Remediated",
        unremediated: "Remediate this vulnerability",
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
          closed: "Safe",
          open: "Vulnerable",
        },
        stateTooltip: {
          closed:
            "The <strong>safe</strong> status means that " +
            "you remediated this type of vulnerability at each location where we reported it.",
          open:
            "The <strong>vulnerable</strong> status means that " +
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
    noFindingsFound: {
      subtitle: "Soon you will see the findings here",
      title: "We are testing your application to find vulnerabilities",
    },
    noneSeverity: "None",
    notificationTable: {
      email: "Email",
      notification: "Notification",
      parameters: {
        minimumSeverity: {
          name: "Minimum severity",
          tooltip:
            "Minimum severity value to send the vulnerability alert " +
            "notification.",
        },
      },
      push: "Push",
      sms: "SMS",
      voice: "Voice",
      whatsapp: "Whatsapp",
    },
    notifyModal: {
      body: "Do you want to send an email notification for this vulnerability",
      cancel: "Cancel",
      notify: "Notify",
    },
    repositoriesTable: {
      state: "State",
    },
    searchPlaceholder: "Search vulnerabilities",
    servicesTable: {
      active: "Active",
      asm: "ARM",
      black: "Black",
      continuous: "Continuous Hacking",
      deleteGroup: {
        alerts: {
          pendingActionsError:
            "Some actions on the group have not been completed. Please try to delete the group later.",
          trialRestrictionError:
            "The action is not allowed during the free trial. Please contact your manager for more details.",
        },
        deleteGroup: "Delete this group",
        reason: {
          diffSectst: "Different security testing strategy",
          migration: "Information will be moved to a different group",
          noSectst: "No more security testing",
          noSystem: "System will be deprecated",
          other: "Other reason not mentioned here",
          rename: "Group rename",
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
        invalidManaged:
          "Incorrect change in managed parameter. Please review the payment conditions",
        organizationNotExists: "Target organization does not exist",
        squadOnlyIfContinuous:
          "Squad is only available in groups of type Continuous-Hacking",
        trial: "You can only have the machine service during the free trial",
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
        warningDowngrade:
          "Disabling ARM will immediately delete the group. " +
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
          "If you do not have more groups, you will be removed from ARM. ",
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
      btsPlaceholder: "https://gitlab.com/fluidattacks/universe/-/issues/2084",
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
      line: "Line",
      linePlural: "Lines",
      markVerified: {
        text: "Verify vulnerabilities",
        tooltip:
          "Assess whether the vulnerability was fixed or not in the current cycle",
      },
      notification: {
        emailNotificationError:
          "There was an error sending the email notification to the assigned",
        emailNotificationText: "Assigned email notification sent successfully",
        emailNotificationTitle: "Notification Status",
      },
      notify: {
        emailNotificationError:
          "There was an error sending the vulnerability notification email",
        emailNotificationText:
          "vulnerability notification email sent successfully",
        emailNotificationTitle: "Notification Status",
        text: "Notify",
        tooltip: "Report the finding to stakeholders in an email notification",
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
        confirmRejectVulnerability: "Confirm/Reject vulnerability",
        confirmRejectZeroRisk: "Confirm/Reject zero risk",
        confirmZeroRisk: "Confirm zero risk",
        inProgress: "In progress",
        new: "Untreated",
        pendingApproval: " (Pending approval)",
        rejectZeroRisk: "Reject zero risk",
        rejected: "Rejected",
        requestZeroRisk: "Request zero risk",
        title: "Treatment",
        untreated: "Untreated",
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
      affectedReattacks: "Reattacks on hold",
      client: "Client",
      comments: "Comments",
      date: "Date reported",
      dateClosed: "Date closed",
      description: "Description",
      edit: "Edit",
      eventIn: "Event present in",
      evidence: "Evidence",
      fluidGroup: "Fluid Attacks' Group",
      hacker: "Hacker",
      id: "ID",
      resume: "Resume",
      root: "Root",
      solvingReason: "Solving reason",
      status: "Status",
      statusValues: {
        pendingVerification: "Pending verification",
        solve: "Solved",
        unsolve: "Unsolved",
      },
      tableAdvice: "Click on an event to see more details",
      type: "Type",
    },
    tabEvidence: {
      altVideo: {
        first: "Here is a",
        second: "link to the video",
        third: "instead.",
      },
      animationExploit: "Exploitation animation",
      date: "Date: ",
      descriptionTooltip: "Brief explanation about the evidence",
      detail: "Detail",
      editable: "Edit",
      editableTooltip: "Modify the evidence for this finding",
      evidenceExploit: "Exploitation evidence",
      fields: {
        modal: {
          continue: "Continue",
          error: "Invalid file.",
          message:
            "Are you sure this is the correct evidence corresponding to this type?",
          title: "Preview new evidence",
        },
      },
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
      baseUrlPlaceholder: "gitlab.com/fluidattacks/universe.git",
      branch: {
        label: "Branch",
        tooltip: "Target branch",
      },
      branchPlaceholder: "main",
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
      common: {
        deactivation: {
          other: "What?",
          reason: {
            accessGranted: "Access granted",
            clonedSuccessfully: "Cloned successfully",
            credentialsAreWorkingNow: "Credentials are working now",
            dataUpdated: "Data updated",
            environmentIsWorkingNow: "Environment is working now",
            installerIsWorkingNow: "Installer is working now",
            isOkToResume: "Is ok to resume",
            label: "Reason",
            newCredentialsProvided: "New credentials provided",
            newEnvironmentProvided: "New environment provided",
            other: "Other",
            permissionDenied: "Permission denied",
            permissionGranted: "Permission granted",
            problemSolved: "Problem solved",
            removedFromScope: "Affected resource removed from scope",
            suppliesWereGiven: "Supplies were given",
            toeApproved: "ToE change approved",
            toeUnchanged: "ToE will remain unchanged",
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
      open: "Open",
      pending: "Pending",
      status: "Status",
      tabTitle: "Tracking",
      tooltip:
        "Evolution of the finding over time: historical records, " +
        "vulnerable/safe vulnerabilities status , " +
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
        disabled: "Please choose only one user to edit",
        text: "Edit",
        tooltip: "Select a user and edit their information",
      },
      editStakeholderTitle: "Edit stakeholder information",
      noSelection: "You must select an email from the table.",
      removeUserButton: {
        confirmMessage: "will be removed from this group",
        confirmTitle: "Remove stakeholder?",
        // eslint-disable-next-line camelcase -- It is required for react-i18next
        confirmTitle_plural: "Remove stakeholder?",
        text: "Remove",
        tooltip: "Remove a user from the group, first select one",
      },
      success: "An invitation email will be sent to",
      successAdmin: "Stakeholder information updated.",
      successDelete: " was removed from this group.",
      successDeletePlural:
        "Many users were successfully removed from this group.",
      textbox: "Email address (Azure, Google or Bitbucket)",
      title: "Add stakeholder to this group",
      titleSuccess: "Success",
    },
    tabVuln: {
      additionalInfo: {
        alerts: {
          updatedDetails: "The vulnerability details have been updated",
        },
        buttons: {
          cancel: {
            text: "Cancel",
            tooltip: "Cancel changes",
          },
          edit: {
            text: "Edit",
            tooltip: "Edit vulnerability",
          },
          save: {
            text: "Save",
            tooltip: "Save changes",
          },
        },
      },
      alerts: {
        acceptanceNotRequested: "Indefinite acceptance is not requested",
        acceptanceSuccess: "Indefinite acceptance has been handled",
        hasNewVulns:
          "Untreated, please select a treatment for the vulnerability.",
        // eslint-disable-next-line camelcase -- It is required for react-i18next
        hasNewVulns_plural:
          "One or more vulnerabilities are set as untreated, please select a treatment for the vulnerabilities.",
        maximumNumberOfAcceptances:
          "Vulnerability has been accepted the maximum number of times allowed by the defined policy",
        tagReminder:
          "Remember to add tags to your vulnerabilities to ease their management",
        treatmentChange: "Vulnerability treatment will be changed",
        uploadFile: {
          addressAndPortDoNotExist:
            "Address and port for the new vulnerabilities of port type must exist on the port surface, error is located at '{{path}}'\n",
          inputUrlAndFieldDoNotExist:
            "URL and field for the new vulnerabilities of input type must exist on the input surface, error is located at '{{path}}'\n",
          invalidRoot:
            "Active root not found for the repo. Verify the nickname in the scope tab\n",
          invalidStream:
            "Invalid stream, it must start with 'home' or 'query', error is located at {{path}}\n",
          key: "Key '{{key}}' located at '{{path}}' is missing or invalid.\n",
          lineDoesNotExistInLoc:
            "The line '{{line}}' does not exist in the range of 0 and lines of code from the lines surface, error is located at '{{path}}'\n",
          linesPathDoesNotExist:
            "Path for the new vulnerabilities of lines type must exist on the lines surface, error is located at '{{path}}'\n",
          missingFindingInfo:
            "Please provide {{missingFields}} before updating\n",
          value:
            "Value is invalid, pattern '{{pattern}}' is not followed at '{{path}}'.\n",
        },
      },
      assignedTooltip: "Filter locations based on who is the assigned",
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
      closed: "Safe",
      commitHash: "Commit hash",
      contentTab: {
        code: {
          title: "Code",
          tooltip: "A portion of the vulnerable code",
        },
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
          "Vulnerability cannot be accepted, severity outside of range set by the defined policy",
      },
      handleAcceptanceModal: {
        submittedForm: {
          reject: {
            consistency: {
              info: "There are consistency issues with the vulnerabilities, the severity or the evidence",
              text: "Consistency",
            },
            evidence: {
              info: "The evidence is insufficient",
              text: "Evidence",
            },
            naming: {
              info: "The vulnerabilities should be submitted under another Finding type",
              text: "Naming",
            },
            omission: {
              info: "More data should be gathered before submission",
              text: "Omission",
            },
            other: {
              info: "Another reason",
              text: "Other",
            },
            reasonForRejection: "Reason for rejection",
            scoring: {
              info: "Faulty severity scoring",
              text: "Scoring",
            },
            why: "Why?",
            writing: {
              info: "The writing could be improved",
              text: "Writing",
            },
          },
          submittedTable: {
            acceptance: "Acceptance",
            confirm: "Confirm",
            confirmed: "Confirmed",
            reject: "Reject",
            rejected: "Rejected",
            specific: "Specific",
            where: "Where",
          },
        },
      },
      info: {
        text: "Please select vulnerabilities to reattack",
        title: "Info",
      },
      notApplicable: "n/a",
      onHold: "On Hold",
      open: "Vulnerable",
      rejected: "Rejected",
      requested: "Requested",
      safe: "Safe",
      searchTag: "Search Tag",
      searchText: "Search Text",
      status: "Status",
      statusTooltip:
        "Filter vulnerabilities based on their vulnerable / safe status (It limits the total results)",
      submitted: "Submitted",
      tabTitle: "Locations",
      tagTooltip: "Filter vulnerabilities based on their tag",
      tooltip: "Vulnerable / Safe vulnerabilities",
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
        source: "Source",
        specific: "Specific",
        specificType: {
          app: "Input",
          code: "LoC",
          infra: "Port",
        },
        status: "Status",
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
        vulnerability: "Vulnerability",
        vulnerabilitySource: {
          ANALYST: "Analyst",
          CUSTOMER: "Customer",
          DETERMINISTIC: "Deterministic",
          ESCAPE: "Escape",
          MACHINE: "Machine",
        },
        vulnerabilityType: {
          inputs: "app",
          lines: "code",
          ports: "infra",
          title: "Type",
        },
        where: "Location",
      },
      vulnerable: "Vulnerable",
    },
    usersTable: {
      firstlogin: "First login",
      invitation: "Invitation",
      invitationState: "Registration status",
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
        country: "Country",
        invalidName: "Name must contain only alphanumeric characters",
        name: "Organization name",
        nameTaken: "Name already taken. Please try with a new one",
        namesUnavailable:
          "There are no available organization names at the moment",
        success: "Organization {{name}} created successfully",
        successTitle: "Success",
        title: "New organization",
        trial: "You can only have one organization during the free trial",
      },
      text: "New Org...",
      tooltip: "Create new organization",
    },
  },
  signup: {
    enrolledUser: {
      button: "Go to the ARM dashboard",
      subtitle:
        " is already registered in the Attack " +
        "Resistance Management platform.",
      title: "Oops! You're not eligible for the free trial.",
    },
    subtitle:
      "Search for vulnerabilities in your application for FREE and " +
      "enjoy all Machine Plan benefits:",
    title: "Start your 21-day trial",
  },
  table: {
    allOptions: "--All options--",
    clearFilters: "Clear Filters",
    filters: "Filters",
    noDataIndication: "There is no data to display",
    results: {
      text: "Showing {{matches}} matching results out of {{total}}",
      tooltip: "The total result is a partial amount until loading all data",
    },
    search: "Search",
    tooltip: "Search filters for the table",
  },
  tagIndicator: {
    acceptedVulnerabilitiesBySeverity:
      "Accepted vulnerabilities by CVSS severity",
    acceptedVulnerabilitiesByUser: "Accepted vulnerabilities by user",
    assignedVulnerabilities: "Vulnerabilities by assignment",
    assignedVulnerabilitiesStatus: "Status of assigned vulnerabilities",
    findingsGroup: "Vulnerability types by group",
    groupsAvailability: "Overall availability of groups",
    meanRemediate: "Mean time to remediate (MTTR) by CVSS severity",
    oldestEvent: "Days since group is failing",
    oldestGroupEvent: "Days since groups are failing",
    openFindingsGroup: "Open vulnerability types by group",
    openVulnsGroups: "Open vulnerabilities by group",
    remediatedAcceptedVuln: "Distribution of vulnerabilities by group",
    reportTechnique: "Report Technique",
    topOldestFindings: "Oldest vulnerability types",
    undefinedTitle: "Undefined Treatment by Group",
    vulnerabilitiesByLevel: "Vulnerabilities by level",
    vulnerabilitiesByTag: "Vulnerabilities by tag",
    vulnerabilitiesByType: "Vulnerabilities by source",
    vulnsGroups: "Vulnerabilities by group",
  },
  taskContainer: {
    filters: {
      dateRange: {
        placeholder: "Report date (range)",
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
  todoList: {
    tabs: {
      drafts: {
        organization: "Organization",
        stateDate: "State Date",
        title: "Drafts",
      },
      reattacks: "Reattacks",
      vulnerabilities: "Vulnerabilities",
    },
    title: "To-Do",
    tooltip: {
      drafts: "Drafts in all your groups",
      reattacks: "Findings with pending reattacks",
      vulnerabilities: "Vulnerabilities assigned to you",
    },
  },
  tours: {
    addGitRoot: {
      addButton: "Now, let’s add your repository so we can analyze your code. ",
      healthCheckConditions:
        "Check all the conditions that apply to your Health Check selection. ",
      intro:
        "Before you start the testing service in your project, " +
        "you need to add the repository or environment to include in the testing. ",
      nickname:
        "This repository name is already in use in your organization. " +
        "Please enter a nickname to differentiate this one from the other.",
      proceedButton: {
        invalidForm:
          "Some of the entered information could not be validated. " +
          "Please, click “Back” and review the entered data or “Close” to abort the guided process. ",
        validForm: "Click “Proceed” to start cloning and analyzing your code. ",
      },
      rootBranch:
        "Enter the repository branch you want to analyze. For example: main. ",
      rootCredentials: {
        content:
          "Enter the credentials that will be used to clone the repository. ",
        invalid: "Enter a valid credential and press check button",
        key: "Paste a valid SSH key.",
        name: "Enter a credential name.",
        token: "Enter a valid repository token and azure organization.",
        type: "Select a credential type.",
        user: "Enter a valid user and password.",
      },
      rootEnvironment:
        "Name the type of environment this branch syncs to. For example: Production. ",
      rootHasHealthCheck:
        "For repositories with existing code, decide if we are going to analyze the existing code " +
        "or only the new work from this point onward. ",
      rootUrl:
        "Start by entering a valid URL of the code repository you need to analyze. " +
        "For example: https://gitlab.com/fluidattacks/universe. ",
      vpn: "Check if access to the repository is done through a VPN. ",
    },
    addGroup: {
      addButton:
        'Let us guide you through the process of setting up your project. Click "New group" to get started!',
      groupDescription:
        "Add a name and description to help you recognize which one of your projects this group is associated with.",
      intro:
        "Each organization on ARM has different groups, " +
        "representing unique projects created by our clients to manage their vulnerabilities separately. ",
      proceedButton: "Click “Proceed” to create your new group. ",
      reportLanguage: "Select your preferred language for reports. ",
      serviceType:
        "Select the type of service for this group. " +
        "Continuous Hacking involves searching for vulnerabilities at set frequencies throughout the project lifecycle, " +
        "whereas One-Shot Hacking searches for them in just one specific version of your project.",
      squadPlan:
        "Squad plan is for clients that want to discover more varied, " +
        "even more complex vulnerabilities through ethical hacking.",
      testingType:
        "Select the type of testing for this group. In Black-box testing, " +
        "we evaluate the application without knowledge of its internal workings and without credentials, " +
        "whereas White-box testing requires them.",
    },
  },
  updateAccessToken: {
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
    tokenLastUsed: "Token last used: ",
    warning: "Warning!",
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
    emailText: "Email address (Azure, Google or Bitbucket)",
    organization: "Organization",
    responsibility: "Responsibility",
    responsibilityPlaceholder: "Product Owner, Group Manager, Tester, ...",
    role: "Role",
    roles: {
      admin: "Admin",
      architect: "Architect",
      customerManager: "Customer Manager",
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
    addFindingModal: {
      duplicatedDescription:
        "Another vulnerability, which has the same title, contains the same description",
      duplicatedRecommendation:
        "Another vulnerability, which has the same title, contains the same recommendation",
      invalidTitle: "The title is not valid",
    },
    alphabetic: "Only alphabetic characters",
    alphanumeric: "Only alphanumeric characters",
    amountOfFiles: "The amount of files must be {{count}} or less",
    between: "This value must be between {{min}} and {{max}}",
    columns: "At least 1 column must be shown",
    commitHash: "The commit hash is invalid",
    credentialsModal: {
      includeLowercase: "Should include lowercase characters",
      includeNumber: "Should include at least one number",
      includeSymbols:
        "Should include symbols characters '~:;%@_$#!,.*-?\"[]|()/{}>^<=&+`",
      includeUppercase: "Should include uppercase characters",
      sequentialsCharacters: "Should not include sequentials characters",
      startWithLetter: "Should start with a letter",
    },
    datetime: "The datetime format is not valid",
    datetimeBetween: "The datetime must be between {{from}} and {{to}}",
    draftTitle: "The title format is not valid",
    draftTypology: "The vulnerability typology is not valid",
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
    hasDraftsRejected:
      "You cannot created a new draft. Review rejected drafts first.",
    inactiveSession:
      "You will be logged out for inactivity in a minute. Click on Dismiss if you wish to stay logged in.",
    inactiveSessionDismiss: "Dismiss",
    inactiveSessionModal: "Inactive Session Detected",
    infectedFile: "Our system detected that the uploaded file is infected",
    integer: "This field can only contain an integer",
    invalidChar:
      "Invalid characters, use: alphanumerics, spaces and punctuations",
    invalidCommentParent: "The comment parent is invalid",
    invalidCredentialName:
      "There is credentials with the same name in the organization",
    invalidCredentialType:
      "Invalid Credential Type for URL, if protocol is ssh: type must not be OAUTH",
    invalidEmailInField: "The email address inserted is not valid",
    invalidEnvironmentUrl: "The environment URL is invalid",
    invalidFieldLength: "The value inserted in one or more fields is invalid",
    invalidMarkdown: "Invalid or malformed markdown",
    invalidPhoneNumber: "The phone number is invalid",
    invalidSpaceField: "This field cannot contain only blankspaces",
    invalidSpaceInField: "This field cannot contain blank spaces",
    invalidSshFormat: "Invalid or malformed SSH private key",
    invalidTextBeginning:
      "Field cannot begin with the following character: {{ chars }}",
    invalidTextField:
      "Field cannot contain the following characters: {{chars}}",
    invalidTextPattern:
      "Field cannot contain the following character pattern: {{ chars }}",
    invalidUrl: "Invalid Url",
    invalidUrlField:
      "URL value cannot contain the following characters: {{chars}}",
    invalidUrlType: "Invalid Url Type",
    invalidValueInField: "The value inserted in one of the fields is not valid",
    location: "The location should not start with = or /",
    lowerDate: "Invalid date",
    maxLength: "Type {{count}} characters or less",
    minLength: "Type {{count}} characters or more",
    noFluidAttacksHackersInFluidAttacksService:
      "Groups with any active Fluid Attacks service " +
      "can only have Hackers provided by Fluid Attacks",
    numeric: "This field can only contain numbers",
    oneOf: "This field must be one of the suggested values",
    portRange: "This field can only contain ports",
    positive: "The number must be greater than 0",
    requestedTooSoon:
      "Please wait a minute before resending an invitation to this user",
    requireNickname: "Nickname already exist",
    required: "Required field",
    someRequired: "Select at least one value",
    stakeholderHasGroupAccess:
      "The stakeholder has been granted access to the group previously",
    stakeholderHasOrganizationAccess:
      "The stakeholder has been granted access to the organization previously",
    tags: "This field can only contain alphanumeric characters and dashes",
    text: "Only alphanumerics, spaces and punctuations",
    unsanitizedInputFound:
      "Invalid characters, avoid the use of =, +, @, commas, semicolons," +
      "tabs + or carriage returns in sensitive fields",
    userIsNotFromFluidAttacks:
      "This role can only be granted to Fluid Attacks users",
    validDate: "The date must be below six months",
    validDateToken: "The date must be below six months",
    validSessionDate: "The session has expired",
    vulnerabilityAlreadyExists: "The vulnerability already exists",
    zeroOrPositive: "The number must be either 0 or positive",
  },
  verifyDialog: {
    alerts: {
      nonSentVerificationCode: "Try again in a few minutes",
      sendMobileVerificationSuccess:
        "A verification code has been sent to your mobile",
    },
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

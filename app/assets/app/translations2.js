/*
 * This file does not allow exports or globals.
 */
/* eslint-disable no-unused-vars */
const translations2 = {
  "search_events": {
    "headings": {
      "date": "Date",
      "details": "Description",
      "id": "ID",
      "status": "Status",
      "type": "Type"
    }
  },
  "search_findings":
 {
   "environment_table": {"environment": "Environment"},
   "filter_labels":
    {
      "cardinalities": "Open Vulnerabilities",
      "cardinalitiesTooltip": "Vulnerabilities pending to be resolved",
      "closure": "Fixed vulnerabilities",
      "closureTooltip": "Percentage of reported vulnerabilities " +
                        "that are already fixed",
      "compromisedRecords": "Total Compromised Records",
      "compromisedRecordsTooltip": "Total compromised records " +
                                    "reported in the project",
      "criticity": "Total Severity Found",
      "criticityTooltip": "Severity of project against the average " +
                          "(<100% safer,> 100% more insecure)",
      "findings": "Findings",
      "findingsTooltip": "Security vulnerabilities reported by category",
      "maximumSeverity": "Maximum Severity Found",
      "maximumSeverityTooltip": "Maximum severity found based on CVSS standard",
      "oldestFinding": "Day(s) from the Oldest Open Finding",
      "oldestFindingTooltip": "Oldest open vulnerability since report date",
      "openEvents": "Open Eventualities",
      "openEventsTooltip": "Events that interfere in the normal " +
                            "execution of project",
      "vulnerabilities": "Total Vulnerabilities",
      "vulnerabilitiesTooltip": "Total reported vulnerabilities"
    },
   "filter_menu": {
     "search": {
       "button": "Search",
       "placeholder": "FLUID project name"
     }
   },
   "headings": {
     "action": "Action",
     "age": "Age (Days)",
     "cardinality": "Open Vuln.",
     "criticity": "Severity",
     "exploit": "Exploitable",
     "finding": "Title",
     "lastVulnerability": "Last Report (Days)",
     "released": "Released",
     "state": "Status",
     "timestamp": "Date",
     "treatment": "Treatment",
     "type": "Type",
     "vulnerability": "Description"
   },
   "page_head": {"breadcrumb": {"project": "Project"}},
   "pop_table":
    {
      "date": "Date",
      "details": "Description",
      "status": "Status",
      "type": "Type"
    },
   "project_buttons": {
     "accept": "Accept",
     "back": "Back",
     "delete": "Delete"
   },
   "project_labels":
    {
      "client": "Customer's Project",
      "criticity": "Severity",
      "project": "FLUID's Project",
      "report": "Report Date",
      "status": "Status",
      "type": "Type",
      "vulnerabilities": "Open Vulnerabilities"
    },
   "repositories_table": {
     "branch": "Branch",
     "repository": "Repository"
   },
   "tab_comments": {"comments_name": "Comments"},
   "tab_cssv2":
      {
        "authentication": "Authentication",
        "availability": "Availability Impact",
        "complexity": "Access Complexity",
        "confidence": "Confidence Level",
        "confidenciality": "Confidentiality Impact",
        "description_name": "Severity",
        "editable": "Edit",
        "exploitability": "Exploitability",
        "integrity": "Integrity Impact",
        "resolution": "Resolution Level",
        "update": "Update",
        "vector": "Access Vector"
      },
   "tab_description":
     {
       "actorTooltip": "Person who could execute the attack vector using " +
                        "the finding which affects the specified targets",
       "btsTooltip": "Link to an external bugtracking system",
       "bts_external": "BTS External",
       "cardinality": "Open Vulnerabilities",
       "category": "Category",
       "compromisedAtributes": "Compromised Atributes",
       "compromisedAtributesTooltip": "Attributes that were compromised when " +
                                      "exploiting the vulnerability",
       "compromisedRecords": "Compromised Records",
       "compromisedRecordsTooltip": "Number of compromised data when " +
                                    "exploiting the vulnerability",
       "description": "Description",
       "descriptionTooltip": "Finding description",
       "description_name": "Description",
       "detailed": "Detailed",
       "edit_treatment": "Edit",
       "editable": "Edit",
       "general": "General",
       "probability": "Probability",
       "recommendation": "Recommendation",
       "recommendationTooltip": "General recommendation given to avoid this " +
                                "security failure",
       "remediated": "Request Verification",
       "remediated_finding": "Finding remediated",
       "requirements": "Requirements",
       "requirementsTooltip": "Security criteria requirement responsible " +
                              "of risk",
       "risk": "Risk Value",
       "severity": "Severity",
       "solution": "Applied Solution Justification",
       "stage": "Scenario",
       "stageTooltip": "Place from where the vulnerability is exploited",
       "system": "Affected Systems",
       "systemTooltip": "Name of the systems that were affected while " +
                        "exploiting this finding",
       "threat": "Threat",
       "threatTooltip": "Description of the threat caused by this security " +
                        "failure",
       "title": "Title",
       "treat_justification": "Treatment Justification",
       "treat_justificationTooltip": "Justification of the treatment that " +
                                      "will be given to the finding",
       "treat_manager": "Treatment Manager",
       "treat_managerTooltip": "Person who defined or modified the treatment " +
                                "that will be given to the finding",
       "treatment": "Treatment",
       "treatmentTooltip": "Treatment that will be given to the finding",
       "type": "Finding Type",
       "update": "Update",
       "update_treatment": "Update",
       "update_treatmodal": "Update Treatment",
       "vectors": "Attack Vectors",
       "vectorsTooltip": "Description of the abuse case generated by " +
                          "this finding",
       "verified": "Verified",
       "verified_finding": "Finding verified",
       "weakness": "Weakness",
       "weaknessTooltip": "Link to a description by the CWE of this " +
                          "vulnerability",
       "where": "Where",
       "whereTooltip": "URL and/or ports of the resources that have " +
                        "security vulnerabilities"
     },
   "tab_evidence":
       {
         "alert": "In progress...",
         "animation_exploit": "Exploitation animation",
         "detail": "Detail",
         "editable": "Edit",
         "evidence_exploit": "Exploitation evidence",
         "evidence_name": "Evidence",
         "update": "Update"
       },
   "tab_observations": {"observations_name": "Observations"},
   "tab_records": {"records_name": "Records"},
   "tab_resources":
   {
     "add_repository": "Add",
     "branch": "Branch",
     "environment": "Environment",
     "environments": "Environments",
     "no_selection": "You must select an item from the table.",
     "password": "Password",
     "remove_repository": "Remove",
     "repositories": "Repositories",
     "repository": "Repository",
     "success": "Item added successfully.",
     "success_remove": "Item removed successfully.",
     "title_env": "Add environment information",
     "title_repo": "Add repository information",
     "username": "Username"
   },
   "tab_tracking":
     {
       "cicle": "Cycle",
       "close": "Closed",
       "closingEffectiveness": "Effectiveness",
       "finding": "Discovery",
       "open": "Open",
       "tracking_name": "Tracking"
     },
   "tab_users": {
     "add_button": "Add",
     "admin": "Admin",
     "analyst": "Analyst",
     "assign_error": "You can only set one administrator at a time.",
     "customer": "User",
     "customer_admin": "Manager",
     "days_ago": " day(s) ago",
     "developer": "Developer",
     "edit": "Edit",
     "edit_user_title": "Edit user information",
     "email": "someone@domain.com",
     "email_title": "Email",
     "error_phone": "The phone number must not contain letters or special " +
                    "characters",
     "hours_ago": " hour(s) ago",
     "minutes_ago": " minute(s) ago",
     "months_ago": " month(s) ago",
     "no_selection": "You must select an email from the table.",
     "phone_number": "Phone Number",
     "remove_admin": "Remove admin",
     "remove_admin_error": "You can only remove one administrator at a time.",
     "remove_user": "Remove",
     "requiered_field": "This field is required.",
     "responsibility_placeholder": "Product Owner, Project Manager, " +
                                    "Tester, ...",
     "role": "Role",
     "success": " now has access to this project.",
     "success_admin": "User information updated.",
     "success_admin_remove": " is no longer an administrator of this project.",
     "success_delete": " was removed from this project.",
     "textbox": "Enter the email of the person you wish to add, it must be " +
                  "an Office 365 or Google email.",
     "title": "Add user to this project",
     "title_success": "Congratulations",
     "undefined": "-",
     "user_max_responsibility": "You must enter a responsibility of maximum " +
                                "50 characters",
     "user_organization": "Organization",
     "user_responsibility": "Responsibility",
     "wrong_format": "The email format is not valid."
   }
 },
  "tab_container": {
    "eventualities": "Events",
    "findings": "Findings",
    "indicators": "Indicators",
    "resources": "Resources",
    "users": "Users"
  }
};

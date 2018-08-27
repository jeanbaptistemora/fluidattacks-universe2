/*
 * This file does not allow exports or globals.
 */
/* eslint-disable no-unused-vars */
const translations1 = {
  "confirmmodal":
   {
     "accept_draft": "Accept Draft",
     "cancel": "Cancel",
     "confirm": "Are you sure?",
     "delete_draft": "Delete Draft",
     "no": "No",
     "proceed": "Proceed",
     "title_cssv2": "Update CSSv2",
     "title_description": "Update Description",
     "title_finding": "Delete Finding",
     "title_project": "Delete Project",
     "yes": "Yes"
   },
  "deletemodal":
   {
     "change_evidence": "Change of evidence",
     "duplicated": "It is duplicated",
     "finding_changed": "Finding has changed",
     "justification": "Justification",
     "not_vulnerability": "It is not a Vulnerability"

   },
  "eventFormstack":
{
  "status": {
    "solve": "Solved",
    "unknown": "-",
    "unsolve": "Unsolved"
  },
  "type":
   {
     "approv_change": "Client approves the change of ToE",
     "auth_attack": "Authorization for special attack",
     "cancel_proj": "Client cancels the project/milestone",
     "det_attack": "Client detects an attack",
     "explic_suspend": "Client explicitly suspends project",
     "high_approval": "High availability approval",
     "inacc_ambient": "Inaccessible ambient",
     "incor_supplies": "Incorrect or missing supplies",
     "other": "other",
     "toe_differs": "ToE differs from what was approved",
     "unknown": "-",
     "uns_ambient": "Unstable ambient"
   }
},
  "event_by_name":
   {
     "btn_group": {
       "edit": "EDIT!",
       "resume": "RESUME!",
       "watch": "WATCH!"
     },
     "modal_avance": {"title": "Events Resume"},
     "modal_edit":
        {
          "close": "Close",
          "refresh": "Update"
        },
     "modal_ver":
      {
        "affec": "Affectation",
        "analyst": "Analyst",
        "c_proj": "Customer's Project",
        "client": "Client",
        "date": "Date",
        "detail": "Description",
        "f_proj": "FLUID's Project",
        "ok": "OK",
        "type": "Type"
      }
   },
  "finding_formstack":
   {
     "access_vector":
      {
        "adjacent": "0.646 | Adjacent network: Exploitable from " +
                    "same network segment",
        "default": "-",
        "local": "0.395 | Local: Exploitable with local access to the target",
        "network": "1.000 | Network: Exploitable from Internet"
      },
     "actor":
      {
        "any_access": "Anyone with access to the station",
        "any_costumer": "Any costumer of the organization",
        "any_employee": "Any employee of the organization",
        "any_internet": "Anyone on Internet",
        "default": "-",
        "one_employee": "Only one employee",
        "some_costumer": "Only some costumers of the organization",
        "some_employee": "Only some employees"
      },
     "authentication":
      {
        "any_authen": "0.704 | None: Authentication is not required",
        "default": "-",
        "multiple_authen": "0.450 | Multiple: Multiple authentication points",
        "single_authen": "0.560 | Single: Single authentication point"
      },
     "availability":
       {
         "complete": "0.660 | Complete: There is a total target fallen",
         "default": "-",
         "none": "0 | None: There is no impact",
         "partial": "0.275 | Partial: There is intermittency in the " +
                    "access to the target"
       },
     "category":
        {
          "avoid_technical": "Avoid exposing the technical information of " +
                             "the application, servers and platforms.",
          "default": "-",
          "define_model": "Define the authorization model considering the " +
                          "principle of minimum privilege",
          "event": "Event",
          "exclude_data": "Exclude sensitive data from source " +
                          "code and event log",
          "maintain": "Maintainability",
          "performance": "Performance",
          "record_event": "Record events for traceability and audit",
          "secure_protoc": "Use secure communication protocols",
          "strengt_authen": "Strengthen controls in authentication and " +
                            "session management",
          "strengt_process": "Strengthen controls in file processing",
          "strengt_protect": "Strengthen the protection of stored data " +
                             "related to passwords or cryptographic keys",
          "update_base": "Update and configure components security baselines",
          "validate_http": "Validate the integrity of transactions " +
                           "in HTTP requests",
          "validate_input": "Implement controls to validate input data"
        },
     "complexity":
           {
             "default": "-",
             "high_complex": "0.350 | High: Special conditions are required " +
                             "like administrative access",
             "low_complex": "0.710 | Low: No special conditions are required",
             "medium_complex": "0.610 | Medium: Some conditions are required " +
                               "like system access"
           },
     "confidence":
       {
         "confirmed": "1.000 | Confirmed: The vulnerability is recognized by " +
                      "the manufacturer",
         "default": "-",
         "not_confirm": "0.900 | Not confirmed: There are few sources that " +
                        "recognize vulnerability",
         "not_corrob": "0.950 | Not corroborared: Vulnerability is " +
                       "recognized by unofficial sources"
       },
     "confidenciality":
        {
          "complete": "0.660 | Complete: Total control over information " +
                      "related with the target",
          "default": "-",
          "none": "0 | None: There is no impact",
          "partial": "0.275 | Partial: Access to information but no " +
                     "control over it"
        },
     "criticity_header": {
       "high": " High",
       "moderate": " Moderate",
       "tolerable": " Tolerable"
     },
     "exploitability":
      {
        "conceptual": "0.900 | Conceptual: There are laboratory tests",
        "default": "-",
        "functional": "0.950 | Functional: There is an exploit",
        "high": "1.000 | High: Exploit is not required or it can be automated",
        "improbable": "0.850 | Improbable: There is no exploit"
      },
     "exploitable": {
       "default": "-",
       "no": "No",
       "yes": "Yes"
     },
     "findingType": {
       "default": "-",
       "hygiene": "Hygiene",
       "vuln": "Vulnerability"
     },
     "integrity":
      {
        "complete": "0.660 | Complete: Posibility of modify all target " +
                    "information",
        "default": "-",
        "none": "0 | None: There is no impact",
        "partial": "0.275 | Partial: Posibility of modify some " +
                   "target information"
      },
     "probability":
       {
         "default": "-",
         "diffic_vuln": "25% Difficult to have a vulnerability",
         "easy_vuln": "75% Easy to have a vulnerability",
         "possible_vuln": "50% Possible vulnerability",
         "prev_vuln": "100% previously with vulnerability"
       },
     "resolution":
       {
         "default": "-",
         "non_existent": "1.000 | Non-existent: There is no solution",
         "official": "0.870 | Official: There is an manufacturer " +
                     "available patch",
         "palliative": "0.950 | Palliative: There is a patch that was not " +
                       "published by the manufacturer",
         "temporal": "0.900 | Temporal: There are temporary solutions"
       },
     "scenario":
      {
        "anon_inter": "Anonymous from Internet",
        "anon_intra": "Anonymous from Intranet",
        "auth_inter": "Authorized Internet user",
        "auth_intra": "Authorized Intranet user",
        "default": "-",
        "infra_scan": "Infrastructure scan",
        "unauth_extra": "Unauthorized Extranet user",
        "unauth_inter": "Unauthorized Internet user"
      },
     "status":
      {
        "close": "Closed",
        "default": "-",
        "open": "Open",
        "part_close": "Partially closed"
      },
     "test_method":
      {
        "analysis": "Analysis",
        "app": "App",
        "binary": "Binary",
        "code": "Code",
        "default": "-",
        "infras": "Infrastructure"
      },
     "treatment_header":
      {
        "asummed": "Accepted",
        "default": "-",
        "remediated": "In Progress",
        "working": "New"
      }
   },
  "forms":
   {
     "closure": "Closure",
     "events": "Events",
     "findings": "Findings",
     "progress": "Progress"
   },
  "grapExploit":
   {
     "exploit_label": "Yes",
     "nonexploit_label": "Not",
     "title": "Exploitability"
   },
  "grapStatus":
   {
     "close_label": "Closed",
     "open_label": "Open",
     "partial_label": "Partial",
     "title": "Status"
   },
  "grapType":
   {
     "hig_label": "Hygiene",
     "seg_label": "Vulnerability",
     "title": "Type"
   },
  "left_menu": {
    "first": "Projects",
    "third": "Forms"
  },
  "legalNotice":
   {
     "acceptBtn":
     {
       "text": "Accept and continue",
       "tooltip": "Click if you understand and accept the terms above"
     },
     "description": "Integrates, Copyright (c) 2018 FLUID. This platform " +
     "contains information proprietary of Fluidsignal Group. " +
     "The client is only allowed to use such information for " +
     "documentation purposes and without disclosing its content " +
     "to third parties because it may contain ideas, concepts, prices " +
     "and/or structures propriety of Fluidsignal Group S.A. Its " +
     "'proprietary' classification means that this information will " +
     "only be used by those who it was meant for. In case of requiring " +
     "total or partial reproductions it must be done with express " +
     "and written authorization of Fluidsignal Group S.A. The rules " +
     "that fundament the classification of information are articles 72, " +
     "Cartagena's agreement 344 of 1.993, article 238 of penal code and " +
     "articles 16 and its following ones from 256 law of 1.996.",
     "rememberCbo":
     {
       "text": "Remember my decision",
       "tooltip": "Mark the checkbox if you want this decision to be permanent"
     },
     "title": "Legal notice"
   },
  "logout":
   {
     "cancel": "Cancel",
     "message": "Are you sure?",
     "ok": "Logout",
     "title": "Close Session"
   },
  "main_content":
   {
     "eventualities":
      {
        "descPluralAlert1": "There are ",
        "descPluralAlert2": "open events that compromise the " +
                            "appropriate performance of the project, " +
                            "please give it the appropriate treatment.",
        "descSingularAlert1": "Attention! ",
        "descSingularAlert2": "There is ",
        "descSingularAlert3": "open event that compromises the " +
                              "appropriate performance of the " +
                              "project, please give it the " +
                              "appropriate treatment."
      },
     "projects":
      {
        "description1": "You can check the details of a project by ",
        "description2": "clicking",
        "description3": " on it",
        "project_description": "Description",
        "project_title": "FLUID's Project",
        "title": "My Projects"
      }
   },
  "progress_mod": {
    "finding": "Finding",
    "title": "Progress Report"
  },
  "proj_alerts":
   {
     "access_denied": "Access denied or project not found",
     "attentTitle": "Attention!",
     "attent_cont": "Empty search",
     "congratulation": "Congratulations",
     "differ_comment": "You must enter a new treatment justification",
     "emptyField": "You must enter an afectation",
     "empty_comment": "You must enter a treatment justification!",
     "errorUpdatingEvent": "An error occurred updating events",
     "error_severity": "Severity must be an integer bewteen 0 and 5",
     "error_text": "There is an error",
     "error_textsad": "There is an error :(",
     "eventExist": "This project has no eventualities",
     "eventFormstack": "Unable to access Formstack",
     "eventPositiveint": "Affectation must be a positive integer or zero",
     "eventUpdated": "Event updated",
     "file_size": "The file size must be less than 10mb",
     "file_size_png": "The image size must be less than 2mb",
     "file_size_py": "The file size must be less than 1mb",
     "file_type_csv": "The file must be .csv type",
     "file_type_gif": "The image must be .gif type",
     "file_type_png": "The image must be .png type",
     "file_type_py": "The file must be .py type",
     "file_type_wrong": "The file has an unknown or non-allowed format",
     "no_file_update": "Failed to update the file",
     "no_finding": "We could not find the finding!",
     "no_text_update": "Failed to update the description",
     "not_found": "The project does not have findings",
     "project_deleted": "Project Deleted",
     "remediated_success": "This finding was marked as remediated. A request " +
                           "to verify the solution was sent",
     "search_cont": "Searching Project...",
     "search_title": "News!",
     "short_comment": "You must enter a justification of at least 30 " +
                       "characters",
     "short_remediated_comment": "You must enter a justification of at least " +
                                 "100 characters",
     "updatedTitle": "Correct!",
     "updated_cont": "Updated ;)",
     "updated_cont_description": "Description Updated ;)",
     "updated_cont_file": "File Updated ;)",
     "updated_treat": "Treatment updated",
     "verified_success": "This finding was marked as verified.",
     "wrong_severity": "You must calculate severity correctly"
   },
  "registration":
   {
     "continue_btn": "Continue as",
     "greeting": "Hello",
     "logged_in_message": "Please log out before trying to access with " +
                          "another account.",
     "logged_in_title": "You are already logged in",
     "not_authorized": "You do not have authorization for login yet. " +
                       "Please contact FLUID's staff or your project " +
                       "administrator to get access."
   },
  "reports":
    {
      "executive_report_mod":
      {
        "message": "The project's documentation has not been finished",
        "title": "Executive Reports"
      },
      "technical_report_mod":
      {
        "body_1": "Technical report is protected by password. The password " +
                  "is the date of  report's PDF generation and your username.",
        "body_2": "Example: someone@fluidattacks.com generates the technical " +
                  "report on 03/15/2018 therefore, the password " +
                  "is 15032018someone",
        "title": "Technical Reports"
      },
      "title": "Reports"
    }
};

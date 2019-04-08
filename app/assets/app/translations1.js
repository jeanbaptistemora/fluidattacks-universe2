/*
 * This file does not allow exports or globals.
 */
/* eslint-disable no-unused-vars */
const translations1 = {
  "finding_formstack":
   {
     "exploitable": {
       "default": "-",
       "no": "No",
       "yes": "Yes"
     },
     "findingType": {
       "default": "-",
       "hygiene": "Hygiene",
       "security": "Security"
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
        "auth_extra": "Authorized Extranet user",
        "auth_inter": "Authorized Internet user",
        "auth_intra": "Authorized Intranet user",
        "default": "-",
        "infra_scan": "Infrastructure scan",
        "unauth_extra": "Unauthorized Extranet user",
        "unauth_inter": "Unauthorized Internet user",
        "unauth_intra": "Unauthorized Intranet user"
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
        "accepted": "Accepted",
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
     "seg_label": "Security",
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
     "description": "Integrates, Copyright (c) 2019 Fluid Attacks. " +
     "This platform contains information proprietary of Fluid Attacks. " +
     "The client is only allowed to use such information for " +
     "documentation purposes and without disclosing its content " +
     "to third parties because it may contain ideas, concepts, prices " +
     "and/or structures propriety of Fluid Attacks. Its " +
     "'proprietary' classification means that this information will " +
     "only be used by those who it was meant for. In case of requiring " +
     "total or partial reproductions it must be done with express " +
     "and written authorization of Fluid Attacks. The rules " +
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
        "project_title": "Fluid's Project",
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
     "file_type_yaml": "The file must be .yaml or .yml type",
     "invalid_schema": "Uploaded file does not match with the schema",
     "no_file_update": "Failed to update the file",
     "no_finding": "We could not find the finding!",
     "no_text_update": "Failed to update the description",
     "project_deleted": "Project Deleted",
     "range_error": "Range limits are wrong",
     "remediated_success": "This finding was marked as remediated. A request " +
                           "to verify the solution was sent",
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
                       "Please contact Fluid Attacks' staff or your project " +
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

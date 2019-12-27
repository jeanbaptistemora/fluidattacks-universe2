import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import { IProjectDraftsAttr } from "../scenes/Dashboard/containers/ProjectDraftsView/types";
import { IProjectFindingsAttr } from "../scenes/Dashboard/containers/ProjectFindingsView/types";
import { IUsersAttr } from "../scenes/Dashboard/containers/ProjectUsersView/types";
import { ISeverityAttr, ISeverityField } from "../scenes/Dashboard/containers/SeverityView/types";
import { msgError } from "./notifications";
import rollbar from "./rollbar";
import translate from "./translations/translate";

type IUserList = IUsersAttr["project"]["users"];

export const formatUserlist:
((userList: IUserList) => IUserList) = (userList: IUserList): IUserList => userList.map((user: IUserList[0]) => {
  const role: string = translate.t(`search_findings.tab_users.${user.role}`);
  const lastLoginDate: number[] = JSON.parse(user.lastLogin);
  let DAYS_IN_MONTH: number;
  DAYS_IN_MONTH = 30;
  let lastLogin: string; lastLogin = "";
  let firstLogin: string; firstLogin = "";
  if (!_.isUndefined(user.firstLogin)) {
    firstLogin = user.firstLogin.split(" ")[0];
  }
  if (lastLoginDate[0] >= DAYS_IN_MONTH) {
    const ROUNDED_MONTH: number = Math.round(lastLoginDate[0] / DAYS_IN_MONTH);
    lastLogin = translate.t("search_findings.tab_users.months_ago", {count: ROUNDED_MONTH});
  } else if (lastLoginDate[0] > 0 && lastLoginDate[0] < DAYS_IN_MONTH) {
    lastLogin = translate.t("search_findings.tab_users.days_ago", {count: lastLoginDate[0]});
  } else if (lastLoginDate[0] === -1) {
    lastLogin = "-";
    firstLogin = "-";
  } else {
    let SECONDS_IN_HOUR: number;
    SECONDS_IN_HOUR = 3600;
    const ROUNDED_HOUR: number = Math.round(lastLoginDate[1] / SECONDS_IN_HOUR);
    let SECONDS_IN_MINUTES: number;
    SECONDS_IN_MINUTES = 60;
    const ROUNDED_MINUTES: number = Math.round(lastLoginDate[1] / SECONDS_IN_MINUTES);
    lastLogin = ROUNDED_HOUR >= 1 && ROUNDED_MINUTES >= SECONDS_IN_MINUTES
    ? translate.t("search_findings.tab_users.hours_ago", {count: ROUNDED_HOUR})
    : translate.t("search_findings.tab_users.minutes_ago", {count: ROUNDED_MINUTES});
  }

  return { ...user, role, lastLogin, firstLogin };
});

export const castFieldsCVSS3: ((dataset: ISeverityAttr["finding"]["severity"]) => ISeverityField[]) =
  (dataset: ISeverityAttr["finding"]["severity"]): ISeverityField[] => {

  const attackVector: {[value: string]: string} = {
    0.85: "search_findings.tab_severity.attack_vector_options.network",
    0.62: "search_findings.tab_severity.attack_vector_options.adjacent",
    0.55: "search_findings.tab_severity.attack_vector_options.local",
    0.2: "search_findings.tab_severity.attack_vector_options.physical",
  };

  const attackComplexity: {[value: string]: string} = {
    0.77: "search_findings.tab_severity.attack_complexity_options.low",
    0.44: "search_findings.tab_severity.attack_complexity_options.high",
  };

  const userInteraction: {[value: string]: string} = {
    0.85: "search_findings.tab_severity.user_interaction_options.none",
    0.62: "search_findings.tab_severity.user_interaction_options.required",
  };

  const severityScope: {[value: string]: string} = {
    0: "search_findings.tab_severity.severity_scope_options.unchanged",
    1: "search_findings.tab_severity.severity_scope_options.changed",
  };

  const confidentialityImpact: {[value: string]: string} = {
    0: "search_findings.tab_severity.confidentiality_impact_options.none",
    0.22: "search_findings.tab_severity.confidentiality_impact_options.low",
    0.56: "search_findings.tab_severity.confidentiality_impact_options.high",
  };

  const integrityImpact: {[value: string]: string} = {
    0: "search_findings.tab_severity.integrity_impact_options.none",
    0.22: "search_findings.tab_severity.integrity_impact_options.low",
    0.56: "search_findings.tab_severity.integrity_impact_options.high",
  };

  const availabilityImpact: {[value: string]: string} = {
    0: "search_findings.tab_severity.availability_impact_options.none",
    0.22: "search_findings.tab_severity.availability_impact_options.low",
    0.56: "search_findings.tab_severity.availability_impact_options.high",
  };

  const exploitability: {[value: string]: string} = {
    1: "search_findings.tab_severity.exploitability_options.high",
    0.97: "search_findings.tab_severity.exploitability_options.functional",
    0.94: "search_findings.tab_severity.exploitability_options.proof_of_concept",
    0.91: "search_findings.tab_severity.exploitability_options.unproven",
  };

  const remediationLevel: {[value: string]: string} = {
    1: "search_findings.tab_severity.remediation_level_options.unavailable",
    0.97: "search_findings.tab_severity.remediation_level_options.workaround",
    0.96: "search_findings.tab_severity.remediation_level_options.temporary_fix",
    0.95: "search_findings.tab_severity.remediation_level_options.official_fix",
  };

  const reportConfidence: {[value: string]: string} = {
    1: "search_findings.tab_severity.report_confidence_options.confirmed",
    0.96: "search_findings.tab_severity.report_confidence_options.reasonable",
    0.92: "search_findings.tab_severity.report_confidence_options.unknown",
  };

  const fields: ISeverityField[] = [
    {
      currentValue: dataset.attackVector, name: "attackVector",
      options: attackVector,
      title: translate.t("search_findings.tab_severity.attack_vector"),
    },
    {
      currentValue: dataset.attackComplexity, name: "attackComplexity",
      options: attackComplexity,
      title: translate.t("search_findings.tab_severity.attack_complexity"),
    },
    {
      currentValue: dataset.userInteraction, name: "userInteraction",
      options: userInteraction,
      title: translate.t("search_findings.tab_severity.user_interaction"),
    },
    {
      currentValue: dataset.severityScope, name: "severityScope",
      options: severityScope,
      title: translate.t("search_findings.tab_severity.severity_scope"),
    },
    {
      currentValue: dataset.confidentialityImpact, name: "confidentialityImpact",
      options: confidentialityImpact,
      title: translate.t("search_findings.tab_severity.confidentiality_impact"),
    },
    {
      currentValue: dataset.integrityImpact, name: "integrityImpact",
      options: integrityImpact,
      title: translate.t("search_findings.tab_severity.integrity_impact"),
    },
    {
      currentValue: dataset.availabilityImpact, name: "availabilityImpact",
      options: availabilityImpact,
      title: translate.t("search_findings.tab_severity.availability_impact"),
    },
    {
      currentValue: dataset.exploitability, name: "exploitability",
      options: exploitability,
      title: translate.t("search_findings.tab_severity.exploitability"),
    },
    {
      currentValue: dataset.remediationLevel, name: "remediationLevel",
      options: remediationLevel,
      title: translate.t("search_findings.tab_severity.remediation_level"),
    },
    {
      currentValue: dataset.reportConfidence, name: "reportConfidence",
      options: reportConfidence,
      title: translate.t("search_findings.tab_severity.report_confidence"),
    },
  ];

  return fields;
};

export const castEnvironmentCVSS3Fields: ((dataset: ISeverityAttr["finding"]["severity"]) => ISeverityField[]) =
  (dataset: ISeverityAttr["finding"]["severity"]): ISeverityField[] => {

  const attackVector: {[value: string]: string} = {
    0.85: "search_findings.tab_severity.attack_vector_options.network",
    0.62: "search_findings.tab_severity.attack_vector_options.adjacent",
    0.55: "search_findings.tab_severity.attack_vector_options.local",
    0.2: "search_findings.tab_severity.attack_vector_options.physical",
  };

  const attackComplexity: {[value: string]: string} = {
    0.77: "search_findings.tab_severity.attack_complexity_options.low",
    0.44: "search_findings.tab_severity.attack_complexity_options.high",
  };

  const userInteraction: {[value: string]: string} = {
    0.85: "search_findings.tab_severity.user_interaction_options.none",
    0.62: "search_findings.tab_severity.user_interaction_options.required",
  };

  const severityScope: {[value: string]: string} = {
    0: "search_findings.tab_severity.severity_scope_options.unchanged",
    1: "search_findings.tab_severity.severity_scope_options.changed",
  };

  const confidentialityImpact: {[value: string]: string} = {
    0: "search_findings.tab_severity.confidentiality_impact_options.none",
    0.22: "search_findings.tab_severity.confidentiality_impact_options.low",
    0.56: "search_findings.tab_severity.confidentiality_impact_options.high",
  };

  const integrityImpact: {[value: string]: string} = {
    0: "search_findings.tab_severity.integrity_impact_options.none",
    0.22: "search_findings.tab_severity.integrity_impact_options.low",
    0.56: "search_findings.tab_severity.integrity_impact_options.high",
  };

  const availabilityImpact: {[value: string]: string} = {
    0: "search_findings.tab_severity.availability_impact_options.none",
    0.22: "search_findings.tab_severity.availability_impact_options.low",
    0.56: "search_findings.tab_severity.availability_impact_options.high",
  };

  const confidentialityRequirement: {[value: string]: string} = {
    1.5: "search_findings.tab_severity.confidentiality_requirement_options.high",
    1: "search_findings.tab_severity.confidentiality_requirement_options.medium",
    0.5: "search_findings.tab_severity.confidentiality_requirement_options.low",
  };

  const integrityRequirement: {[value: string]: string} = {
    1.5: "search_findings.tab_severity.integrity_requirement_options.high",
    1: "search_findings.tab_severity.integrity_requirement_options.medium",
    0.5: "search_findings.tab_severity.integrity_requirement_options.low",
  };

  const availabilityRequirement: {[value: string]: string} = {
    1.5: "search_findings.tab_severity.availability_requirement_options.high",
    1: "search_findings.tab_severity.availability_requirement_options.medium",
    0.5: "search_findings.tab_severity.availability_requirement_options.low",
  };

  const fields: ISeverityField[] = [
    {
      currentValue: dataset.confidentialityRequirement, name: "confidentialityRequirement",
      options: confidentialityRequirement,
      title: translate.t("search_findings.tab_severity.confidentiality_requirement"),
    },
    {
      currentValue: dataset.integrityRequirement, name: "integrityRequirement",
      options: integrityRequirement,
      title: translate.t("search_findings.tab_severity.integrity_requirement"),
    },
    {
      currentValue: dataset.availabilityRequirement, name: "availabilityRequirement",
      options: availabilityRequirement,
      title: translate.t("search_findings.tab_severity.availability_requirement"),
    },
    {
      currentValue: dataset.modifiedAttackVector, name: "modifiedAttackVector",
      options: attackVector,
      title: translate.t("search_findings.tab_severity.modified_attack_vector"),
    },
    {
      currentValue: dataset.modifiedAttackComplexity, name: "modifiedAttackComplexity",
      options: attackComplexity,
      title: translate.t("search_findings.tab_severity.modified_attack_complexity"),
    },
    {
      currentValue: dataset.modifiedUserInteraction, name: "modifiedUserInteraction",
      options: userInteraction,
      title: translate.t("search_findings.tab_severity.modified_user_interaction"),
    },
    {
      currentValue: dataset.modifiedSeverityScope, name: "modifiedSeverityScope",
      options: severityScope,
      title: translate.t("search_findings.tab_severity.modified_severity_scope"),
    },
    {
      currentValue: dataset.modifiedConfidentialityImpact, name: "modifiedConfidentialityImpact",
      options: confidentialityImpact,
      title: translate.t("search_findings.tab_severity.modified_confidentiality_impact"),
    },
    {
      currentValue: dataset.modifiedIntegrityImpact, name: "modifiedIntegrityImpact",
      options: integrityImpact,
      title: translate.t("search_findings.tab_severity.modified_integrity_impact"),
    },
    {
      currentValue: dataset.modifiedAvailabilityImpact, name: "modifiedAvailabilityImpact",
      options: availabilityImpact,
      title: translate.t("search_findings.tab_severity.modified_availability_impact"),
    },
  ];

  return fields;
};

export const castEventType: ((field: string) => string) = (field: string): string => {
  const eventType: {[value: string]: string} = {
    "AUTHORIZATION_SPECIAL_ATTACK": "search_findings.tab_events.type_values.auth_attack",
    "Ambiente inestable": "search_findings.tab_events.type_values.uns_ambient",
    "Ambiente no accesible": "search_findings.tab_events.type_values.inacc_ambient",
    "CLIENT_APPROVES_CHANGE_TOE": "search_findings.tab_events.type_values.approv_change",
    "CLIENT_CANCELS_PROJECT_MILESTONE": "search_findings.tab_events.type_values.cancel_proj",
    "CLIENT_DETECTS_ATTACK": "search_findings.tab_events.type_values.det_attack",
    "CLIENT_EXPLICITLY_SUSPENDS_PROJECT": "search_findings.tab_events.type_values.explic_suspend",
    "HIGH_AVAILABILITY_APPROVAL": "search_findings.tab_events.type_values.high_approval",
    "INCORRECT_MISSING_SUPPLIES": "search_findings.tab_events.type_values.incor_supplies",
    "OTHER": "search_findings.tab_events.type_values.other",
    "TOE_DIFFERS_APPROVED": "search_findings.tab_events.type_values.toe_differs",
  };

  return eventType[field];
};

export const castEventStatus: ((field: string) => string) = (field: string): string => {
  const eventStatus: {[value: string]: string} = {
    CREATED: "search_findings.tab_events.status_values.unsolve",
    SOLVED: "search_findings.tab_events.status_values.solve",
  };

  return eventStatus[field];
};

export const castPrivileges:
((scope: string) => {[value: string]: string}) =
  (scope: string): {[value: string]: string} => {
    const privilegesRequiredScope: {[value: string]: string} = {
      0.85: "search_findings.tab_severity.privileges_required_options.none",
      0.68: "search_findings.tab_severity.privileges_required_options.low",
      0.5: "search_findings.tab_severity.privileges_required_options.high",
    };
    const privilegesRequiredNoScope: {[value: string]: string} = {
      0.85: "search_findings.tab_severity.privileges_required_options.none",
      0.62: "search_findings.tab_severity.privileges_required_options.low",
      0.27: "search_findings.tab_severity.privileges_required_options.high",
    };
    const privilegesOptions: {[value: string]: string} = (parseInt(scope, 10) === 1)
      ? privilegesRequiredScope
      : privilegesRequiredNoScope;

    return privilegesOptions;
};

export const formatCweUrl: ((cweId: string) => string) = (cweId: string): string =>
  _.includes(["None", ""], cweId) ? "-" : `https://cwe.mitre.org/data/definitions/${cweId}.html`;

export const formatDropdownField: ((field: string) => string) = (field: string): string => {
  const translationParameters: {[value: string]: string} = {
    "ACCEPTED": "search_findings.tab_description.treatment.accepted",
    "ACCEPTED_UNDEFINED": "search_findings.tab_description.treatment.accepted_undefined",
    "ANONYMOUS_INTERNET": "search_findings.tab_description.scenario.anon_inter",
    "ANONYMOUS_INTRANET": "search_findings.tab_description.scenario.anon_intra",
    "ANYONE_INTERNET": "search_findings.tab_description.actor.any_internet",
    "ANYONE_WORKSTATION": "search_findings.tab_description.actor.any_station",
    "ANY_CUSTOMER": "search_findings.tab_description.actor.any_customer",
    "ANY_EMPLOYEE": "search_findings.tab_description.actor.any_employee",
    "APPLICATIONS": "search_findings.tab_description.ambit.applications",
    "AUTHORIZED_USER_EXTRANET": "search_findings.tab_description.scenario.auth_extra",
    "AUTHORIZED_USER_INTERNET": "search_findings.tab_description.scenario.auth_inter",
    "AUTHORIZED_USER_INTRANET": "search_findings.tab_description.scenario.auth_intra",
    "DATABASES": "search_findings.tab_description.ambit.databases",
    "IN PROGRESS": "search_findings.tab_description.treatment.in_progress",
    "INFRASTRUCTURE": "search_findings.tab_description.ambit.infra",
    "NEW": "search_findings.tab_description.treatment.new",
    "ONE_EMPLOYEE": "search_findings.tab_description.actor.one_employee",
    "REJECTED": "search_findings.tab_description.treatment.rejected",
    "SOME_CUSTOMERS": "search_findings.tab_description.actor.some_customer",
    "SOME_EMPLOYEES": "search_findings.tab_description.actor.some_employee",
    "SOURCE_CODE": "search_findings.tab_description.ambit.sourcecode",
    "UNAUTHORIZED_USER_EXTRANET": "search_findings.tab_description.scenario.unauth_extra",
    "UNAUTHORIZED_USER_INTERNET": "search_findings.tab_description.scenario.unauth_inter",
    "UNAUTHORIZED_USER_INTRANET": "search_findings.tab_description.scenario.unauth_intra",
  };

  return translationParameters[field];
};

export const formatFindingType: ((type: string) => string) = (type: string): string =>
  _.isEmpty(type) ? "-" : translate.t(`search_findings.tab_description.type.${type.toLowerCase()}`);

type IFindingsDataset = IProjectFindingsAttr["project"]["findings"];
export const formatFindings: ((dataset: IFindingsDataset) => IFindingsDataset) =
  (dataset: IFindingsDataset): IFindingsDataset => dataset.map((finding: IFindingsDataset[0]) => {
    const stateParameters: { [value: string]: string } = {
      closed: "search_findings.status.closed",
      open: "search_findings.status.open",
    };
    const treatmentParameters: { [value: string]: string } = {
      "-": (finding.state === "closed") ? "-" : "-",
      "ACCEPTED": (finding.state === "open")
        ? "search_findings.tab_description.treatment.accepted" : "-",
      "ACCEPTED_UNDEFINED": (finding.state === "open")
        ? "search_findings.tab_description.treatment.accepted_undefined" : "-",
      "IN PROGRESS": (finding.state === "open")
        ? "search_findings.tab_description.treatment.in_progress" : "-",
      "NEW": (finding.state === "open")
        ? "search_findings.tab_description.treatment.new" : "-",
    };
    const typeParameters: { [value: string]: string } = {
      HYGIENE: "search_findings.tab_description.type.hygiene",
      SECURITY: "search_findings.tab_description.type.security",
    };
    const state: string = translate.t(stateParameters[finding.state]);
    const treatment: string = translate.t(treatmentParameters[finding.treatment]);
    const type: string = translate.t(typeParameters[finding.type]);
    const isExploitable: string = translate.t(Boolean(finding.isExploitable)
      ? "project.findings.boolean.True" : "project.findings.boolean.False");
    const remediated: string = translate.t(Boolean(finding.remediated)
    ? "project.findings.remediated.True" : "project.findings.remediated.False");

    const where: string = _.uniqBy(finding.vulnerabilities, "where")
      .map((vuln: { where: string }): string => vuln.where)
      .sort()
      .join(", ");

    return { ...finding, state, treatment, type, isExploitable, remediated, where };
  });

type IDraftsDataset = IProjectDraftsAttr["project"]["drafts"];
export const formatDrafts: ((dataset: IDraftsDataset) => IDraftsDataset) =
  (dataset: IDraftsDataset): IDraftsDataset => dataset.map((draft: IDraftsDataset[0]) => {
    const typeParameters: { [value: string]: string } = {
      HYGIENE: "search_findings.tab_description.type.hygiene",
      SECURITY: "search_findings.tab_description.type.security",
    };
    const status: { [value: string]: string } = {
      CREATED: "search_findings.draft_status.created",
      REJECTED: "search_findings.draft_status.rejected",
      SUBMITTED: "search_findings.draft_status.submitted",
    };
    const reportDate: string = draft.reportDate.split(" ")[0];
    const currentState: string = translate.t(status[draft.currentState]);
    const type: string = translate.t(typeParameters[draft.type]);
    const isExploitable: string = translate.t(Boolean(draft.isExploitable)
      ? "project.findings.boolean.True" : "project.findings.boolean.False");

    return { ...draft, reportDate, type, isExploitable, currentState };
  });

export const handleErrors: ((errorText: string, errors: readonly GraphQLError[]) => void) =
  (errorText: string, errors: readonly GraphQLError[]): void => {
    errors.map((err: GraphQLError) => {
      if (_.includes(["Login required", "Exception - Invalid Authorization"], err.message)) {
        location.assign("/integrates/logout");
      } else if (_.includes(
        ["Access denied", "Exception - Project does not exist", "Exception - Finding not found"],
        err.message)) {
        msgError(translate.t("proj_alerts.access_denied"));
      } else if (_.includes("Error in file", err.message)) {
        msgError(translate.t("search_findings.tab_description.errorFileVuln"));
      } else if (_.includes("Exception - Email is not valid", err.message)) {
        msgError(translate.t("validations.email"));
      } else if (_.includes("Exception - Parameter is not valid", err.message)) {
        msgError(translate.t("validations.invalidValueInField"));
      } else if (_.includes("Exception - Invalid Expiration Time", err.message)) {
        msgError(translate.t("update_access_token.invalid_exp_time"));
      } else if (_.includes(err.message, "Exception - This draft has missing fields")) {
        msgError(translate.t("project.drafts.error_submit", {
          missingFields: err.message.split("fields: ")[1],
        }));
      } else {
        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(errorText, err);
      }
    });
  };

export const handleGraphQLErrors: ((errorText: string, error: ApolloError) => void) =
  (errorText: string, error: ApolloError): void => {
    handleErrors(errorText, error.graphQLErrors);
  };

type IEventsDataset = Array<{ eventStatus: string; eventType: string }>;
export const formatEvents: ((dataset: IEventsDataset) => IEventsDataset) =
  (dataset: IEventsDataset): IEventsDataset => dataset.map((event: IEventsDataset[0]) => {
    const eventType: string = translate.t(castEventType(event.eventType));
    const eventStatus: string = translate.t(castEventStatus(event.eventStatus));

    return { ...event, eventType, eventStatus };
  });

import _ from "lodash";
import { IProjectUsersViewProps } from "../scenes/Dashboard/containers/ProjectUsersView";
import { ISeverityField, ISeverityViewProps } from "../scenes/Dashboard/containers/SeverityView";
import translate from "./translations/translate";

export const formatUserlist:
((arg1: IProjectUsersViewProps["userList"]) => IProjectUsersViewProps["userList"]) =
  (userList: IProjectUsersViewProps["userList"]): IProjectUsersViewProps["userList"] => {
  for (const user of userList) {
    user.role = translate.t(`search_findings.tab_users.${user.role}`);
    const lastLoginDate: number[] = JSON.parse(user.lastLogin);
    let DAYS_IN_MONTH: number;
    DAYS_IN_MONTH = 30;

    if (lastLoginDate[0] >= DAYS_IN_MONTH) {
      const ROUNDED_MONTH: number = Math.round(lastLoginDate[0] / DAYS_IN_MONTH);
      user.lastLogin = translate.t("search_findings.tab_users.months_ago", {count: ROUNDED_MONTH});
    } else if (lastLoginDate[0] > 0 && lastLoginDate[0] < DAYS_IN_MONTH) {
      user.lastLogin = translate.t("search_findings.tab_users.days_ago", {count: lastLoginDate[0]});
    } else if (lastLoginDate[0] === -1) {
      user.lastLogin = "-";
      user.firstLogin = "-";
    } else {
      let SECONDS_IN_HOUR: number;
      SECONDS_IN_HOUR = 3600;
      const ROUNDED_HOUR: number = Math.round(lastLoginDate[1] / SECONDS_IN_HOUR);
      let SECONDS_IN_MINUTES: number;
      SECONDS_IN_MINUTES = 60;
      const ROUNDED_MINUTES: number = Math.round(lastLoginDate[1] / SECONDS_IN_MINUTES);
      user.lastLogin = ROUNDED_HOUR >= 1 && ROUNDED_MINUTES >= SECONDS_IN_MINUTES
      ? translate.t("search_findings.tab_users.hours_ago", {count: ROUNDED_HOUR})
      : translate.t("search_findings.tab_users.minutes_ago", {count: ROUNDED_MINUTES});
    }
  }

  return userList;
};

export const castFieldsCVSS2: ((dataset: ISeverityViewProps["dataset"]) => ISeverityField[]) =
  (dataset: ISeverityViewProps["dataset"]): ISeverityField[] => {

  const accessVector: {[value: string]: string} = {
    0.395: "search_findings.tab_severity.vector_options.local",
    0.646: "search_findings.tab_severity.vector_options.adjacent",
    1: "search_findings.tab_severity.vector_options.network",
  };

  const confidentialityImpact: {[value: string]: string} = {
    0: "search_findings.tab_severity.confidentiality_options.none",
    0.275: "search_findings.tab_severity.confidentiality_options.partial",
    0.66: "search_findings.tab_severity.confidentiality_options.complete",
  };

  const integrityImpact: {[value: string]: string} = {
    0: "search_findings.tab_severity.integrity_options.none",
    0.275: "search_findings.tab_severity.integrity_options.partial",
    0.66: "search_findings.tab_severity.integrity_options.complete",
  };

  const availabilityImpact: {[value: string]: string} = {
    0: "search_findings.tab_severity.availability_options.none",
    0.275: "search_findings.tab_severity.availability_options.partial",
    0.66: "search_findings.tab_severity.availability_options.complete",
  };

  const authentication: {[value: string]: string} = {
    0.45: "search_findings.tab_severity.authentication_options.multiple_auth",
    0.56: "search_findings.tab_severity.authentication_options.single_auth",
    0.704: "search_findings.tab_severity.authentication_options.no_auth",
  };

  const exploitability: {[value: string]: string} = {
    0.85: "search_findings.tab_severity.exploitability_options.improbable",
    0.9: "search_findings.tab_severity.exploitability_options.conceptual",
    0.95: "search_findings.tab_severity.exploitability_options.functional",
    1: "search_findings.tab_severity.exploitability_options.high",
  };

  const confidenceLevel: {[value: string]: string} = {
    0.9: "search_findings.tab_severity.confidence_options.not_confirm",
    0.95: "search_findings.tab_severity.confidence_options.not_corrob",
    1: "search_findings.tab_severity.confidence_options.confirmed",
  };

  const resolutionLevel: {[value: string]: string} = {
    0.87: "search_findings.tab_severity.resolution_options.official",
    0.9: "search_findings.tab_severity.resolution_options.temporal",
    0.95: "search_findings.tab_severity.resolution_options.palliative",
    1: "search_findings.tab_severity.resolution_options.non_existent",
  };

  const accessComplexity: {[value: string]: string} = {
    0.35: "search_findings.tab_severity.complexity_options.high_complex",
    0.61: "search_findings.tab_severity.complexity_options.medium_complex",
    0.71: "search_findings.tab_severity.complexity_options.low_complex",
  };

  const fields: ISeverityField[] = [
    {
      currentValue: dataset.accessVector, name: "accessVector",
      options: accessVector,
      title: translate.t("search_findings.tab_severity.vector"),
    },
    {
      currentValue: dataset.confidentialityImpact, name: "confidentialityImpact",
      options: confidentialityImpact,
      title: translate.t("search_findings.tab_severity.confidentiality"),
    },
    {
      currentValue: dataset.integrityImpact, name: "integrityImpact",
      options: integrityImpact,
      title: translate.t("search_findings.tab_severity.integrity"),
    },
    {
      currentValue: dataset.availabilityImpact, name: "availabilityImpact",
      options: availabilityImpact,
      title: translate.t("search_findings.tab_severity.availability"),
    },
    {
      currentValue: dataset.authentication, name: "authentication",
      options: authentication,
      title: translate.t("search_findings.tab_severity.authentication"),
    },
    {
      currentValue: dataset.exploitability, name: "exploitability",
      options: exploitability,
      title: translate.t("search_findings.tab_severity.exploitability"),
    },
    {
      currentValue: dataset.confidenceLevel, name: "confidenceLevel",
      options: confidenceLevel,
      title: translate.t("search_findings.tab_severity.confidence"),
    },
    {
      currentValue: dataset.resolutionLevel, name: "resolutionLevel",
      options: resolutionLevel,
      title: translate.t("search_findings.tab_severity.resolution"),
    },
    {
      currentValue: dataset.accessComplexity, name: "accessComplexity",
      options: accessComplexity,
      title: translate.t("search_findings.tab_severity.complexity"),
    },
  ];

  return fields;
};

export const castFieldsCVSS3: ((dataset: ISeverityViewProps["dataset"]) => ISeverityField[]) =
  (dataset: ISeverityViewProps["dataset"]): ISeverityField[] => {

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

export const castFields:
((dataset: ISeverityViewProps["dataset"], cvssVersion: ISeverityViewProps["cvssVersion"]) => ISeverityField[]) =
  (dataset: ISeverityViewProps["dataset"], cvssVersion: ISeverityViewProps["cvssVersion"]): ISeverityField[] =>
  cvssVersion === "3" ? castFieldsCVSS3(dataset) : castFieldsCVSS2(dataset);

export const castPrivileges:
((dataset: ISeverityViewProps["dataset"], scope: string, modifiedScope: string) => ISeverityField[]) =
  (dataset: ISeverityViewProps["dataset"], scope: string, modifiedScope: string): ISeverityField[] => {
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
    const modifiedPrivilegesOptions: {[value: string]: string} = parseInt(modifiedScope, 10) === 1
      ? privilegesRequiredScope
      : privilegesRequiredNoScope;

    const fields: ISeverityField[] = [
      {
        currentValue: dataset.privilegesRequired, name: "privilegesRequired",
        options: privilegesOptions,
        title: translate.t("search_findings.tab_severity.privileges_required"),
      },
      {
        currentValue: dataset.modifiedPrivilegesRequired, name: "modifiedPrivilegesRequired",
        options: modifiedPrivilegesOptions,
        title: translate.t("search_findings.tab_severity.modified_privileges_required"),
      },
    ];

    return fields;
};
export const formatCweUrl: ((cweId: string) => string) = (cweId: string): string =>
  _.includes(["None", ""], cweId) ? "-" : `https://cwe.mitre.org/data/definitions/${cweId}.html`;

export const formatDropdownField: ((field: string) => string) = (field: string): string => {
  const translationParameters: {[value: string]: string} = {
    "ACCEPTED": "search_findings.tab_description.treatment.accepted",
    "ANONYMOUS_INTERNET": "search_findings.tab_description.scenario.anon_inter",
    "ANONYMOUS_INTRANET": "search_findings.tab_description.scenario.anon_intra",
    "ANYONE_INTERNET": "search_findings.tab_description.actor.any_internet",
    "ANYONE_WORKSTATION": "search_findings.tab_description.actor.any_station",
    "ANY_COSTUMER": "search_findings.tab_description.actor.any_costumer",
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
    "SOME_CUSTOMERS": "search_findings.tab_description.actor.some_costumer",
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

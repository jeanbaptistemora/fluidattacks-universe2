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

export const castFields: ((dataset: ISeverityViewProps["dataset"]) => ISeverityField[]) =
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

export const formatCweUrl: ((cweId: string) => string) = (cweId: string): string =>
  cweId === "-" ? "-" : `https://cwe.mitre.org/data/definitions/${cweId}.html`;

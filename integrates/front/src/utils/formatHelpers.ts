import { translate } from "utils/translations/translate";

const castEventType: (field: string) => string = (field: string): string => {
  const eventType: Record<string, string> = {
    AUTHORIZATION_SPECIAL_ATTACK:
      "search_findings.tab_events.type_values.auth_attack",
    "Ambiente inestable": "search_findings.tab_events.type_values.uns_ambient",
    "Ambiente no accesible":
      "search_findings.tab_events.type_values.inacc_ambient",
    CLIENT_APPROVES_CHANGE_TOE:
      "search_findings.tab_events.type_values.approv_change",
    CLIENT_DETECTS_ATTACK: "search_findings.tab_events.type_values.det_attack",
    HIGH_AVAILABILITY_APPROVAL:
      "search_findings.tab_events.type_values.high_approval",
    INCORRECT_MISSING_SUPPLIES:
      "search_findings.tab_events.type_values.incor_supplies",
    OTHER: "search_findings.tab_events.type_values.other",
    TOE_DIFFERS_APPROVED: "search_findings.tab_events.type_values.toeDiffers",
  };

  return eventType[field];
};

const castEventStatus: (field: string) => string = (field: string): string => {
  const eventStatus: Record<string, string> = {
    CREATED: "search_findings.tab_events.status_values.unsolve",
    SOLVED: "search_findings.tab_events.status_values.solve",
  };

  return eventStatus[field];
};

const formatDropdownField: (field: string) => string = (
  field: string
): string => {
  const translationParameters: Record<string, string> = {
    ACCEPTED: "search_findings.tab_description.treatment.accepted",
    ACCEPTED_UNDEFINED:
      "search_findings.tab_description.treatment.acceptedUndefined",
    ANONYMOUS_INTERNET: "search_findings.tab_description.scenario.anonInter",
    ANONYMOUS_INTRANET: "search_findings.tab_description.scenario.anonIntra",
    ANYONE_INTERNET: "search_findings.tab_description.actor.anyInternet",
    ANYONE_WORKSTATION: "search_findings.tab_description.actor.anyStation",
    ANY_CUSTOMER: "search_findings.tab_description.actor.anyCustomer",
    ANY_EMPLOYEE: "search_findings.tab_description.actor.anyEmployee",
    APPLICATIONS: "search_findings.tab_description.ambit.applications",
    AUTHORIZED_USER_EXTRANET:
      "search_findings.tab_description.scenario.authExtra",
    AUTHORIZED_USER_INTERNET:
      "search_findings.tab_description.scenario.authInter",
    AUTHORIZED_USER_INTRANET:
      "search_findings.tab_description.scenario.authIntra",
    DATABASES: "search_findings.tab_description.ambit.databases",
    INFRASTRUCTURE: "search_findings.tab_description.ambit.infra",
    IN_PROGRESS: "search_findings.tab_description.treatment.inProgress",
    NEW: "search_findings.tab_description.treatment.new",
    ONE_EMPLOYEE: "search_findings.tab_description.actor.oneEmployee",
    REJECTED: "search_findings.tab_description.treatment.rejected",
    SOME_CUSTOMERS: "search_findings.tab_description.actor.someCustomer",
    SOME_EMPLOYEES: "search_findings.tab_description.actor.someEmployee",
    SOURCE_CODE: "search_findings.tab_description.ambit.sourcecode",
    UNAUTHORIZED_USER_EXTRANET:
      "search_findings.tab_description.scenario.unauthExtra",
    UNAUTHORIZED_USER_INTERNET:
      "search_findings.tab_description.scenario.unauthInter",
    UNAUTHORIZED_USER_INTRANET:
      "search_findings.tab_description.scenario.unauthIntra",
  };

  return translationParameters[field];
};

const formatTreatment: (treatment: string, findingState: string) => string = (
  treatment: string,
  findingState: string
): string => {
  const treatmentParameters: Record<string, string> = {
    "-": "-",
    ACCEPTED:
      findingState === "open"
        ? "search_findings.tab_description.treatment.accepted"
        : "-",
    ACCEPTED_UNDEFINED:
      findingState === "open"
        ? "search_findings.tab_description.treatment.acceptedUndefined"
        : "-",
    "ACCEPTED_UNDEFINED pending":
      findingState === "open"
        ? translate.t(
            "search_findings.tab_description.treatment.acceptedUndefined"
          ) +
          translate.t(
            "search_findings.tab_description.treatment.pendingApproval"
          )
        : "-",
    "IN PROGRESS":
      findingState === "open"
        ? "search_findings.tab_description.treatment.inProgress"
        : "-",
    NEW:
      findingState === "open"
        ? "search_findings.tab_description.treatment.new"
        : "-",
  };
  const treatmentRes: string = translate.t(treatmentParameters[treatment]);

  return treatmentRes;
};

export { castEventType, castEventStatus, formatDropdownField, formatTreatment };

import { translate } from "utils/translations/translate";

const castEventType: (field: string) => string = (field: string): string => {
  const eventType: Record<string, string> = {
    AUTHORIZATION_SPECIAL_ATTACK:
      "search_findings.tabEvents.typeValues.authAttack",
    "Ambiente inestable": "search_findings.tabEvents.typeValues.unsAmbient",
    "Ambiente no accesible":
      "search_findings.tabEvents.typeValues.inaccAmbient",
    CLIENT_APPROVES_CHANGE_TOE:
      "search_findings.tabEvents.typeValues.approvChange",
    CLIENT_DETECTS_ATTACK: "search_findings.tabEvents.typeValues.detAttack",
    HIGH_AVAILABILITY_APPROVAL:
      "search_findings.tabEvents.typeValues.highApproval",
    INCORRECT_MISSING_SUPPLIES:
      "search_findings.tabEvents.typeValues.incorSupplies",
    OTHER: "search_findings.tabEvents.typeValues.other",
    TOE_DIFFERS_APPROVED: "search_findings.tabEvents.typeValues.toeDiffers",
  };

  return eventType[field];
};

const castEventStatus: (field: string) => string = (field: string): string => {
  const eventStatus: Record<string, string> = {
    CREATED: "search_findings.tabEvents.statusValues.unsolve",
    SOLVED: "search_findings.tabEvents.statusValues.solve",
  };

  return eventStatus[field];
};

const formatDropdownField: (field: string) => string = (
  field: string
): string => {
  const translationParameters: Record<string, string> = {
    ACCEPTED: "search_findings.tabDescription.treatment.accepted",
    ACCEPTED_UNDEFINED:
      "search_findings.tabDescription.treatment.acceptedUndefined",
    ANONYMOUS_INTERNET: "search_findings.tabDescription.scenario.anonInter",
    ANONYMOUS_INTRANET: "search_findings.tabDescription.scenario.anonIntra",
    ANYONE_INTERNET: "search_findings.tabDescription.actor.anyInternet",
    ANYONE_WORKSTATION: "search_findings.tabDescription.actor.anyStation",
    ANY_CUSTOMER: "search_findings.tabDescription.actor.anyCustomer",
    ANY_EMPLOYEE: "search_findings.tabDescription.actor.anyEmployee",
    APPLICATIONS: "search_findings.tabDescription.ambit.applications",
    AUTHORIZED_USER_EXTRANET:
      "search_findings.tabDescription.scenario.authExtra",
    AUTHORIZED_USER_INTERNET:
      "search_findings.tabDescription.scenario.authInter",
    AUTHORIZED_USER_INTRANET:
      "search_findings.tabDescription.scenario.authIntra",
    DATABASES: "search_findings.tabDescription.ambit.databases",
    INFRASTRUCTURE: "search_findings.tabDescription.ambit.infra",
    IN_PROGRESS: "search_findings.tabDescription.treatment.inProgress",
    NEW: "search_findings.tabDescription.treatment.new",
    ONE_EMPLOYEE: "search_findings.tabDescription.actor.oneEmployee",
    REJECTED: "search_findings.tabDescription.treatment.rejected",
    SOME_CUSTOMERS: "search_findings.tabDescription.actor.someCustomer",
    SOME_EMPLOYEES: "search_findings.tabDescription.actor.someEmployee",
    SOURCE_CODE: "search_findings.tabDescription.ambit.sourcecode",
    UNAUTHORIZED_USER_EXTRANET:
      "search_findings.tabDescription.scenario.unauthExtra",
    UNAUTHORIZED_USER_INTERNET:
      "search_findings.tabDescription.scenario.unauthInter",
    UNAUTHORIZED_USER_INTRANET:
      "search_findings.tabDescription.scenario.unauthIntra",
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
        ? "search_findings.tabDescription.treatment.accepted"
        : "-",
    ACCEPTED_UNDEFINED:
      findingState === "open"
        ? "search_findings.tabDescription.treatment.acceptedUndefined"
        : "-",
    "ACCEPTED_UNDEFINED pending":
      findingState === "open"
        ? translate.t(
            "search_findings.tabDescription.treatment.acceptedUndefined"
          ) +
          translate.t(
            "search_findings.tabDescription.treatment.pendingApproval"
          )
        : "-",
    "IN PROGRESS":
      findingState === "open"
        ? "search_findings.tabDescription.treatment.inProgress"
        : "-",
    NEW:
      findingState === "open"
        ? "search_findings.tabDescription.treatment.new"
        : "-",
  };
  const treatmentRes: string = translate.t(treatmentParameters[treatment]);

  return treatmentRes;
};

export { castEventType, castEventStatus, formatDropdownField, formatTreatment };

import { translate } from "utils/translations/translate";

const castEventType: (field: string) => string = (field: string): string => {
  const eventType: Record<string, string> = {
    AUTHORIZATION_SPECIAL_ATTACK:
      "searchFindings.tabEvents.typeValues.authAttack",
    "Ambiente inestable": "searchFindings.tabEvents.typeValues.unsAmbient",
    "Ambiente no accesible": "searchFindings.tabEvents.typeValues.inaccAmbient",
    CLIENT_APPROVES_CHANGE_TOE:
      "searchFindings.tabEvents.typeValues.approvChange",
    CLIENT_DETECTS_ATTACK: "searchFindings.tabEvents.typeValues.detAttack",
    HIGH_AVAILABILITY_APPROVAL:
      "searchFindings.tabEvents.typeValues.highApproval",
    INCORRECT_MISSING_SUPPLIES:
      "searchFindings.tabEvents.typeValues.incorSupplies",
    OTHER: "searchFindings.tabEvents.typeValues.other",
    TOE_DIFFERS_APPROVED: "searchFindings.tabEvents.typeValues.toeDiffers",
  };

  return eventType[field];
};

const castEventStatus: (field: string) => string = (field: string): string => {
  const eventStatus: Record<string, string> = {
    CREATED: "searchFindings.tabEvents.statusValues.unsolve",
    SOLVED: "searchFindings.tabEvents.statusValues.solve",
  };

  return eventStatus[field];
};

const formatDropdownField: (field: string) => string = (
  field: string
): string => {
  const translationParameters: Record<string, string> = {
    ACCEPTED: "searchFindings.tabDescription.treatment.accepted",
    ACCEPTED_UNDEFINED:
      "searchFindings.tabDescription.treatment.acceptedUndefined",
    ANONYMOUS_INTERNET: "searchFindings.tabDescription.scenario.anonInter",
    ANONYMOUS_INTRANET: "searchFindings.tabDescription.scenario.anonIntra",
    ANYONE_INTERNET: "searchFindings.tabDescription.actor.anyInternet",
    ANYONE_WORKSTATION: "searchFindings.tabDescription.actor.anyStation",
    ANY_CUSTOMER: "searchFindings.tabDescription.actor.anyCustomer",
    ANY_EMPLOYEE: "searchFindings.tabDescription.actor.anyEmployee",
    APPLICATIONS: "searchFindings.tabDescription.ambit.applications",
    AUTHORIZED_USER_EXTRANET:
      "searchFindings.tabDescription.scenario.authExtra",
    AUTHORIZED_USER_INTERNET:
      "searchFindings.tabDescription.scenario.authInter",
    AUTHORIZED_USER_INTRANET:
      "searchFindings.tabDescription.scenario.authIntra",
    DATABASES: "searchFindings.tabDescription.ambit.databases",
    INFRASTRUCTURE: "searchFindings.tabDescription.ambit.infra",
    IN_PROGRESS: "searchFindings.tabDescription.treatment.inProgress",
    NEW: "searchFindings.tabDescription.treatment.new",
    ONE_EMPLOYEE: "searchFindings.tabDescription.actor.oneEmployee",
    REJECTED: "searchFindings.tabDescription.treatment.rejected",
    SOME_CUSTOMERS: "searchFindings.tabDescription.actor.someCustomer",
    SOME_EMPLOYEES: "searchFindings.tabDescription.actor.someEmployee",
    SOURCE_CODE: "searchFindings.tabDescription.ambit.sourcecode",
    UNAUTHORIZED_USER_EXTRANET:
      "searchFindings.tabDescription.scenario.unauthExtra",
    UNAUTHORIZED_USER_INTERNET:
      "searchFindings.tabDescription.scenario.unauthInter",
    UNAUTHORIZED_USER_INTRANET:
      "searchFindings.tabDescription.scenario.unauthIntra",
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
        ? "searchFindings.tabDescription.treatment.accepted"
        : "-",
    ACCEPTED_UNDEFINED:
      findingState === "open"
        ? "searchFindings.tabDescription.treatment.acceptedUndefined"
        : "-",
    "ACCEPTED_UNDEFINED pending":
      findingState === "open"
        ? translate.t(
            "searchFindings.tabDescription.treatment.acceptedUndefined"
          ) +
          translate.t("searchFindings.tabDescription.treatment.pendingApproval")
        : "-",
    "IN PROGRESS":
      findingState === "open"
        ? "searchFindings.tabDescription.treatment.inProgress"
        : "-",
    NEW:
      findingState === "open"
        ? "searchFindings.tabDescription.treatment.new"
        : "-",
  };
  const treatmentRes: string = translate.t(treatmentParameters[treatment]);

  return treatmentRes;
};

export { castEventType, castEventStatus, formatDropdownField, formatTreatment };

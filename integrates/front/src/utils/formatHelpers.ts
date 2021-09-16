import { translate } from "utils/translations/translate";

const castActionAfterBlocking: (field: string) => string = (
  field: string
): string => {
  const eventActionsAfterBlocking: Record<string, string> = {
    EXECUTE_OTHER_GROUP_OTHER_CLIENT:
      "searchFindings.tabEvents.actionAfterBlockingValues.otherOther",
    EXECUTE_OTHER_GROUP_SAME_CLIENT:
      "searchFindings.tabEvents.actionAfterBlockingValues.otherSame",
    EXECUTE_OTHER_PROJECT_OTHER_CLIENT:
      "searchFindings.tabEvents.actionAfterBlockingValues.otherOther",
    EXECUTE_OTHER_PROJECT_SAME_CLIENT:
      "searchFindings.tabEvents.actionAfterBlockingValues.otherSame",
    NONE: "searchFindings.tabEvents.actionAfterBlockingValues.none",
    OTHER: "searchFindings.tabEvents.actionAfterBlockingValues.other",
    TRAINING: "searchFindings.tabEvents.actionAfterBlockingValues.training",
  };

  return eventActionsAfterBlocking[field]
    ? eventActionsAfterBlocking[field]
    : "-";
};

const castActionBeforeBlocking: (field: string) => string = (
  field: string
): string => {
  const eventActionsBeforeBlocking: Record<string, string> = {
    DOCUMENT_GROUP:
      "searchFindings.tabEvents.actionBeforeBlockingValues.documentGroup",
    DOCUMENT_PROJECT:
      "searchFindings.tabEvents.actionBeforeBlockingValues.documentGroup",
    NONE: "searchFindings.tabEvents.actionBeforeBlockingValues.none",
    OTHER: "searchFindings.tabEvents.actionBeforeBlockingValues.other",
    TEST_OTHER_PART_TOE:
      "searchFindings.tabEvents.actionBeforeBlockingValues.testOtherPartToe",
  };

  return eventActionsBeforeBlocking[field]
    ? eventActionsBeforeBlocking[field]
    : "-";
};

const castAffectedComponents: (field: string) => string = (
  field: string
): string => {
  const eventAffectedComponents: Record<string, string> = {
    CLIENT_STATION:
      "searchFindings.tabEvents.affectedComponentsValues.clientStation",
    COMPILE_ERROR:
      "searchFindings.tabEvents.affectedComponentsValues.compileError",
    DOCUMENTATION:
      "searchFindings.tabEvents.affectedComponentsValues.documentation",
    FLUID_STATION:
      "searchFindings.tabEvents.affectedComponentsValues.fluidStation",
    INTERNET_CONNECTION:
      "searchFindings.tabEvents.affectedComponentsValues.internetConnection",
    LOCAL_CONNECTION:
      "searchFindings.tabEvents.affectedComponentsValues.localConnection",
    OTHER: "searchFindings.tabEvents.affectedComponentsValues.other",
    SOURCE_CODE: "searchFindings.tabEvents.affectedComponentsValues.sourceCode",
    TEST_DATA: "searchFindings.tabEvents.affectedComponentsValues.testData",
    TOE_ALTERATION:
      "searchFindings.tabEvents.affectedComponentsValues.toeAlteration",
    TOE_CREDENTIALS:
      "searchFindings.tabEvents.affectedComponentsValues.toeCredentials",
    TOE_EXCLUSSION:
      "searchFindings.tabEvents.affectedComponentsValues.toeExclussion",
    TOE_LOCATION:
      "searchFindings.tabEvents.affectedComponentsValues.toeLocation",
    TOE_PRIVILEGES:
      "searchFindings.tabEvents.affectedComponentsValues.toePrivileges",
    TOE_UNACCESSIBLE:
      "searchFindings.tabEvents.affectedComponentsValues.toeUnaccessible",
    TOE_UNAVAILABLE:
      "searchFindings.tabEvents.affectedComponentsValues.toeUnavailable",
    TOE_UNSTABLE:
      "searchFindings.tabEvents.affectedComponentsValues.toeUnstable",
    VPN_CONNECTION:
      "searchFindings.tabEvents.affectedComponentsValues.vpnConnection",
  };

  return eventAffectedComponents[field] ? eventAffectedComponents[field] : "-";
};

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

const formatAccessibility: (field: string) => string = (
  field: string
): string => {
  const eventAccessibility: Record<string, string> = {
    Ambiente: "group.events.form.accessibility.environment",
    Repositorio: "group.events.form.accessibility.repository",
  };

  return eventAccessibility[field] ? eventAccessibility[field] : "-";
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
    REJECTED: "searchFindings.tabDescription.treatment.rejected",
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

  return translate.t(treatmentParameters[treatment]);
};

export {
  castActionAfterBlocking,
  castActionBeforeBlocking,
  castAffectedComponents,
  castEventType,
  castEventStatus,
  formatAccessibility,
  formatDropdownField,
  formatTreatment,
};

import { castEventType } from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

const selectOptionType = {
  [translate.t("group.events.form.type.specialAttack")]: translate.t(
    castEventType("AUTHORIZATION_SPECIAL_ATTACK")
  ),
  [translate.t("group.events.form.type.toeChange")]: translate.t(
    castEventType("CLIENT_APPROVES_CHANGE_TOE")
  ),
  [translate.t(castEventType("CLIENT_DETECTS_ATTACK"))]: translate.t(
    castEventType("CLIENT_DETECTS_ATTACK")
  ),
  [translate.t("group.events.form.type.highAvailability")]: translate.t(
    castEventType("HIGH_AVAILABILITY_APPROVAL")
  ),
  [translate.t("group.events.form.type.missingSupplies")]: translate.t(
    castEventType("INCORRECT_MISSING_SUPPLIES")
  ),
  [translate.t("group.events.form.type.toeDiffers")]: translate.t(
    castEventType("TOE_DIFFERS_APPROVED")
  ),
  [translate.t("group.events.form.other")]: translate.t(castEventType("OTHER")),
};
const eventActionsBeforeBlocking: Record<string, string> = {
  [translate.t(
    "searchFindings.tabEvents.actionBeforeBlockingValues.documentGroup"
  )]: "searchFindings.tabEvents.actionBeforeBlockingValues.documentGroup",
  [translate.t(
    "searchFindings.tabEvents.actionBeforeBlockingValues.testOtherPartToe"
  )]: "searchFindings.tabEvents.actionBeforeBlockingValues.testOtherPartToe",
  [translate.t("searchFindings.tabEvents.actionBeforeBlockingValues.none")]:
    "searchFindings.tabEvents.actionBeforeBlockingValues.none",
  [translate.t("searchFindings.tabEvents.actionBeforeBlockingValues.other")]:
    "searchFindings.tabEvents.actionBeforeBlockingValues.other",
};
const eventActionsAfterBlocking: Record<string, string> = {
  [translate.t(
    "searchFindings.tabEvents.actionAfterBlockingValues.otherOther"
  )]: "searchFindings.tabEvents.actionAfterBlockingValues.otherOther",
  [translate.t("searchFindings.tabEvents.actionAfterBlockingValues.otherSame")]:
    "searchFindings.tabEvents.actionAfterBlockingValues.otherSame",
  [translate.t(
    "searchFindings.tabEvents.actionAfterBlockingValues.otherOther"
  )]: "searchFindings.tabEvents.actionAfterBlockingValues.otherOther",
  [translate.t("searchFindings.tabEvents.actionAfterBlockingValues.training")]:
    "searchFindings.tabEvents.actionAfterBlockingValues.training",
  [translate.t("searchFindings.tabEvents.actionAfterBlockingValues.none")]:
    "searchFindings.tabEvents.actionAfterBlockingValues.none",
  [translate.t("searchFindings.tabEvents.actionAfterBlockingValues.other")]:
    "searchFindings.tabEvents.actionAfterBlockingValues.other",
};
const accessibilityOptions: Record<string, string> = {
  [translate.t("group.events.form.accessibility.environment")]:
    "group.events.form.accessibility.environment",
  [translate.t("group.events.form.accessibility.repository")]:
    "group.events.form.accessibility.repository",
  "-": "-",
};
const afectCompsOptions: Record<string, string> = {
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.clientStation"
  )]: "searchFindings.tabEvents.affectedComponentsValues.clientStation",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.compileError"
  )]: "searchFindings.tabEvents.affectedComponentsValues.compileError",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.documentation"
  )]: "searchFindings.tabEvents.affectedComponentsValues.documentation",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.fluidStation"
  )]: "searchFindings.tabEvents.affectedComponentsValues.fluidStation",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.internetConnection"
  )]: "searchFindings.tabEvents.affectedComponentsValues.internetConnection",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.localConnection"
  )]: "searchFindings.tabEvents.affectedComponentsValues.localConnection",
  [translate.t("searchFindings.tabEvents.affectedComponentsValues.other")]:
    "searchFindings.tabEvents.affectedComponentsValues.other",
  [translate.t("searchFindings.tabEvents.affectedComponentsValues.sourceCode")]:
    "searchFindings.tabEvents.affectedComponentsValues.sourceCode",
  [translate.t("searchFindings.tabEvents.affectedComponentsValues.testData")]:
    "searchFindings.tabEvents.affectedComponentsValues.testData",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.toeAlteration"
  )]: "searchFindings.tabEvents.affectedComponentsValues.toeAlteration",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.toeCredentials"
  )]: "searchFindings.tabEvents.affectedComponentsValues.toeCredentials",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.toeExclussion"
  )]: "searchFindings.tabEvents.affectedComponentsValues.toeExclussion",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.toeLocation"
  )]: "searchFindings.tabEvents.affectedComponentsValues.toeLocation",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.toePrivileges"
  )]: "searchFindings.tabEvents.affectedComponentsValues.toePrivileges",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.toeUnaccessible"
  )]: "searchFindings.tabEvents.affectedComponentsValues.toeUnaccessible",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.toeUnavailable"
  )]: "searchFindings.tabEvents.affectedComponentsValues.toeUnavailable",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.toeUnstable"
  )]: "searchFindings.tabEvents.affectedComponentsValues.toeUnstable",
  [translate.t(
    "searchFindings.tabEvents.affectedComponentsValues.vpnConnection"
  )]: "searchFindings.tabEvents.affectedComponentsValues.vpnConnection",
  "-": "-",
};

export {
  accessibilityOptions,
  afectCompsOptions,
  eventActionsAfterBlocking,
  eventActionsBeforeBlocking,
  selectOptionType,
};

import { castEventType } from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

const selectOptionType = {
  [translate.t(castEventType("AUTHORIZATION_SPECIAL_ATTACK"))]: translate.t(
    castEventType("AUTHORIZATION_SPECIAL_ATTACK")
  ),
  [translate.t(castEventType("CLIENT_CANCELS_PROJECT_MILESTONE"))]: translate.t(
    castEventType("CLIENT_CANCELS_PROJECT_MILESTONE")
  ),
  [translate.t(castEventType("CLIENT_EXPLICITLY_SUSPENDS_PROJECT"))]:
    translate.t(castEventType("CLIENT_EXPLICITLY_SUSPENDS_PROJECT")),
  [translate.t(castEventType("CLONING_ISSUES"))]: translate.t(
    castEventType("CLONING_ISSUES")
  ),
  [translate.t(castEventType("CREDENTIAL_ISSUES"))]: translate.t(
    castEventType("CREDENTIAL_ISSUES")
  ),
  [translate.t(castEventType("DATA_UPDATE_REQUIRED"))]: translate.t(
    castEventType("DATA_UPDATE_REQUIRED")
  ),
  [translate.t(castEventType("ENVIRONMENT_ISSUES"))]: translate.t(
    castEventType("ENVIRONMENT_ISSUES")
  ),
  [translate.t(castEventType("INCORRECT_MISSING_SUPPLIES"))]: translate.t(
    castEventType("INCORRECT_MISSING_SUPPLIES")
  ),
  [translate.t(castEventType("INSTALLER_ISSUES"))]: translate.t(
    castEventType("INSTALLER_ISSUES")
  ),
  [translate.t(castEventType("MISSING_SUPPLIES"))]: translate.t(
    castEventType("MISSING_SUPPLIES")
  ),
  [translate.t(castEventType("NETWORK_ACCESS_ISSUES"))]: translate.t(
    castEventType("NETWORK_ACCESS_ISSUES")
  ),
  [translate.t(castEventType("OTHER"))]: translate.t(castEventType("OTHER")),
  [translate.t(castEventType("REMOTE_ACCESS_ISSUES"))]: translate.t(
    castEventType("REMOTE_ACCESS_ISSUES")
  ),
  [translate.t(castEventType("TOE_DIFFERS_APPROVED"))]: translate.t(
    castEventType("TOE_DIFFERS_APPROVED")
  ),
  [translate.t(castEventType("VPN_ISSUES"))]: translate.t(
    castEventType("VPN_ISSUES")
  ),
};
const accessibilityOptions: Record<string, string> = {
  [translate.t("group.events.form.accessibility.environment")]:
    "group.events.form.accessibility.environment",
  [translate.t("group.events.form.accessibility.repository")]:
    "group.events.form.accessibility.repository",
  [translate.t("group.events.form.accessibility.vpnConnection")]:
    "group.events.form.accessibility.vpnConnection",
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
};

export { accessibilityOptions, afectCompsOptions, selectOptionType };

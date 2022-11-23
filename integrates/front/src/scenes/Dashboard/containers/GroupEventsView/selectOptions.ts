import { castEventType } from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

const selectOptionType = [
  translate.t(castEventType("AUTHORIZATION_SPECIAL_ATTACK")),
  translate.t(castEventType("CLIENT_CANCELS_PROJECT_MILESTONE")),
  translate.t(castEventType("CLIENT_EXPLICITLY_SUSPENDS_PROJECT")),
  translate.t(castEventType("CLONING_ISSUES")),
  translate.t(castEventType("CREDENTIAL_ISSUES")),
  translate.t(castEventType("DATA_UPDATE_REQUIRED")),
  translate.t(castEventType("ENVIRONMENT_ISSUES")),
  translate.t(castEventType("INSTALLER_ISSUES")),
  translate.t(castEventType("MISSING_SUPPLIES")),
  translate.t(castEventType("NETWORK_ACCESS_ISSUES")),
  translate.t(castEventType("OTHER")),
  translate.t(castEventType("REMOTE_ACCESS_ISSUES")),
  translate.t(castEventType("TOE_DIFFERS_APPROVED")),
  translate.t(castEventType("VPN_ISSUES")),
];

export { selectOptionType };

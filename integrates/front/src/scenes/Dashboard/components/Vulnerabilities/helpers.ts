import type { IErrorInfoAttr } from "./uploadFile";

import { Logger } from "utils/logger";
import { msgError, msgErrorStick } from "utils/notifications";
import { translate } from "utils/translations/translate";

function formatError(errorName: string, errorValue: string): string {
  return ` ${translate.t(errorName)} "${errorValue}" ${translate.t(
    "groupAlerts.invalid"
  )}. `;
}

const errorMessageHelper = (message: string): void => {
  if (message === "Exception - Invalid characters") {
    msgError(translate.t("validations.invalidChar"));
  } else if (message === "Exception - Invalid File Size") {
    msgError(translate.t("validations.fileSize", { count: 1 }));
  } else if (message === "Exception - Invalid File Type") {
    msgError(translate.t("groupAlerts.fileTypeYaml"));
  } else if (message.includes("Exception - Error in path value")) {
    const errorObject: IErrorInfoAttr = JSON.parse(message);
    msgErrorStick(`${translate.t("groupAlerts.pathValue")}
    ${formatError("groupAlerts.value", errorObject.values)}`);
  } else if (message.includes("Exception - Error in port value")) {
    const errorObject: IErrorInfoAttr = JSON.parse(message);
    msgErrorStick(`${translate.t("groupAlerts.portValue")}
    ${formatError("groupAlerts.value", errorObject.values)}`);
  } else if (message === "Exception - Error in specific value") {
    msgError(translate.t("groupAlerts.invalidSpecific"));
  } else if (
    message ===
    "Exception - You can upload a maximum of 100 vulnerabilities per file"
  ) {
    msgError(translate.t("groupAlerts.invalidNOfVulns"));
  } else if (message === "Exception - Error Uploading File to S3") {
    msgError(translate.t("groupAlerts.errorTextsad"));
  } else if (message === "Exception - Invalid Stream") {
    translate.t("groupAlerts.invalidSchema");
    msgError(
      translate.t("searchFindings.tabVuln.alerts.uploadFile.invalidStream")
    );
  } else if (message === "Exception - Access denied or root not found") {
    msgError(
      translate.t("searchFindings.tabVuln.alerts.uploadFile.invalidRoot")
    );
  } else {
    msgError(translate.t("groupAlerts.invalidSpecific"));
    Logger.warning(message);
  }
};

export { errorMessageHelper };

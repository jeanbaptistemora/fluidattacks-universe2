import type React from "react";
import type { UseTranslationResponse } from "react-i18next";

import type { IErrorInfoAttr } from "./uploadFile";

import type { IRemoveVulnAttr } from "../RemoveVulnerability/types";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { getVulnerabilityById } from "scenes/Dashboard/components/Vulnerabilities/utils";
import { Logger } from "utils/logger";
import { msgError, msgErrorStick, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

function formatError(errorName: string, errorValue: string): string {
  return ` ${translate.t(errorName)} "${errorValue}" ${translate.t(
    "groupAlerts.invalid"
  )}. `;
}

const errorMessageHelper = (message: string): void => {
  if (message.includes("Exception - Error in path value")) {
    const errorObject: IErrorInfoAttr = JSON.parse(message);
    msgErrorStick(`${translate.t("groupAlerts.pathValue")}
    ${formatError("groupAlerts.value", errorObject.values)}`);
  } else if (message.includes("Exception - Error in port value")) {
    const errorObject: IErrorInfoAttr = JSON.parse(message);
    msgErrorStick(`${translate.t("groupAlerts.portValue")}
    ${formatError("groupAlerts.value", errorObject.values)}`);
  } else if (
    message.includes(
      "Exception - Invalid stream should start 'home' or 'query'"
    )
  ) {
    const destructMsg: { msg: string; path: string } = JSON.parse(message);
    msgError(
      translate.t("searchFindings.tabVuln.alerts.uploadFile.invalidStream", {
        path: destructMsg.path,
      })
    );
  } else {
    switch (message) {
      case "Exception - Access denied or root not found":
        msgError(
          translate.t("searchFindings.tabVuln.alerts.uploadFile.invalidRoot")
        );
        break;
      case "Exception - Error in specific value":
        msgError(translate.t("groupAlerts.invalidSpecific"));
        break;
      case "Exception - Error Uploading File to S3":
        msgError(translate.t("groupAlerts.errorTextsad"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
        break;
      case "Exception - Invalid File Size":
        msgError(translate.t("validations.fileSize", { count: 1 }));
        break;
      case "Exception - Invalid File Type":
        msgError(translate.t("groupAlerts.fileTypeYaml"));
        break;
      case "Exception - The commit hash is invalid":
        msgError(translate.t("groupAlerts.invalidCommitHash"));
        break;
      case "Exception - You can upload a maximum of 100 vulnerabilities per file":
        msgError(translate.t("groupAlerts.invalidNOfVulns"));
        break;
      case "Expected path to start with the repo nickname":
        msgError(translate.t("groupAlerts.expectedPathToStartWithRepo"));
        break;
      case "Expected vulnerability to have repo_nickname":
        msgError(translate.t("groupAlerts.expectedVulnToHaveNickname"));
        break;
      case "Invalid, only New vulnerabilities with Open state are allowed":
        msgError(translate.t("groupAlerts.onlyNewVulnerabilitiesOpenState"));
        break;
      case "Invalid, you cannot change the nickname while closing":
        msgError(
          translate.t("groupAlerts.invalidCannotModifyNicknameWhenClosing")
        );
        break;
      default:
        msgError(translate.t("groupAlerts.invalidSpecific"));
        Logger.error(
          "An error occurred uploading vulnerabilities file",
          message
        );
        break;
    }
  }
};

const onRemoveVulnResultHelper = (
  removeVulnResult: IRemoveVulnAttr,
  t: UseTranslationResponse<"translation">["t"]
): void => {
  if (removeVulnResult.removeVulnerability.success) {
    msgSuccess(
      t("searchFindings.tabDescription.vulnDeleted"),
      t("groupAlerts.titleSuccess")
    );
  } else {
    msgError(t("deleteVulns.notSuccess"));
  }
};

const handleDeleteVulnerabilityHelper = (
  vulnInfo: Record<string, string> | undefined,
  setVulnerabilityId: (value: React.SetStateAction<string>) => void,
  setDeleteVulnOpen: (value: React.SetStateAction<boolean>) => void,
  updateRow: (value: React.SetStateAction<IVulnRowAttr | undefined>) => void,
  vulnerabilities: IVulnRowAttr[]
): void => {
  if (vulnInfo !== undefined) {
    const vulnerability: IVulnRowAttr | undefined = getVulnerabilityById(
      vulnerabilities,
      vulnInfo.id
    );
    if (vulnerability !== undefined) {
      updateRow(vulnerability);
    }
    setVulnerabilityId(vulnInfo.id);
    setDeleteVulnOpen(true);
  }
};

const setColumnHelper = (
  isEditing: boolean,
  columnHelper: () => JSX.Element
): JSX.Element | undefined => {
  if (isEditing) {
    return columnHelper();
  }

  return undefined;
};

export {
  errorMessageHelper,
  handleDeleteVulnerabilityHelper,
  onRemoveVulnResultHelper,
  setColumnHelper,
};

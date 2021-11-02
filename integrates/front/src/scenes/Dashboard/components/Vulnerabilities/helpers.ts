import type React from "react";
import type { UseTranslationResponse } from "react-i18next";

import type { IErrorInfoAttr } from "./uploadFile";

import type { IRemoveVulnAttr } from "../RemoveVulnerability/types";
import type {
  IVulnDataTypeAttr,
  IVulnRowAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  getNonSelectableVulnerabilitiesOnEdit,
  getNonSelectableVulnerabilitiesOnReattack,
  getNonSelectableVulnerabilitiesOnVerify,
  getVulnerabilitiesIds,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { Logger } from "utils/logger";
import { msgError, msgErrorStick, msgSuccess } from "utils/notifications";
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
  } else if (message === "Expected path to start with the repo nickname") {
    msgError(translate.t("groupAlerts.expectedPathToStartWithRepo"));
  } else if (message === "Expected vulnerability to have repo_nickname") {
    msgError(translate.t("groupAlerts.expectedVulnToHaveNickname"));
  } else if (
    message === "Invalid, you cannot change the nickname while closing"
  ) {
    msgError(translate.t("groupAlerts.invalidCannotModifyNicknameWhenClosing"));
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
    Logger.error("An error occurred uploading vulnerabilities file", message);
  }
};

function setNonSelectable(
  vulns: IVulnRowAttr[],
  requestingReattack: boolean,
  verifyingRequest: boolean
): number[] {
  const nonSelectable: number[] = getNonSelectableVulnerabilitiesOnEdit(vulns);
  if (requestingReattack) {
    return [
      ...getNonSelectableVulnerabilitiesOnReattack(vulns),
      ...nonSelectable,
    ];
  } else if (verifyingRequest) {
    return [
      ...getNonSelectableVulnerabilitiesOnVerify(vulns),
      ...nonSelectable,
    ];
  }

  return nonSelectable;
}

const onRemoveVulnResultHelper = (
  removeVulnResult: IRemoveVulnAttr,
  t: UseTranslationResponse<"translation", undefined>["t"]
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

const onSelectVariousVulnerabilitiesHelper = (
  isSelect: boolean,
  vulnerabilitiesSelected: IVulnRowAttr[],
  selectedVulnerabilities: IVulnRowAttr[],
  setSelectedVulnerabilities: (
    value: React.SetStateAction<IVulnRowAttr[]>
  ) => void
): string[] => {
  if (isSelect) {
    const vulnsToSet: IVulnRowAttr[] = Array.from(
      new Set([...selectedVulnerabilities, ...vulnerabilitiesSelected])
    );
    setSelectedVulnerabilities(vulnsToSet);

    return vulnsToSet.map((vuln: IVulnRowAttr): string => vuln.id);
  }
  const vulnerabilitiesIds: string[] = getVulnerabilitiesIds(
    vulnerabilitiesSelected
  );
  setSelectedVulnerabilities(
    Array.from(
      new Set(
        selectedVulnerabilities.filter(
          (selectedVulnerability: IVulnDataTypeAttr): boolean =>
            !vulnerabilitiesIds.includes(selectedVulnerability.id)
        )
      )
    )
  );

  return selectedVulnerabilities.map((vuln: IVulnRowAttr): string => vuln.id);
};

const handleDeleteVulnerabilityHelper = (
  vulnInfo: Record<string, string> | undefined,
  setVulnerabilityId: (value: React.SetStateAction<string>) => void,
  setDeleteVulnOpen: (value: React.SetStateAction<boolean>) => void
): void => {
  if (vulnInfo !== undefined) {
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
  onSelectVariousVulnerabilitiesHelper,
  setColumnHelper,
  setNonSelectable,
};

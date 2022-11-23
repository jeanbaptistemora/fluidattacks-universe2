import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { useFormikContext } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IConfirmButtonsProps } from "./types";

import type { IUpdateVulnerabilityForm } from "../../types";
import { ModalConfirm } from "components/Modal/Confirm";
import { authzPermissionsContext } from "utils/authz/config";

const ConfirmButtons: React.FC<IConfirmButtonsProps> = ({
  deletingTag,
  handleCloseModal,
  isDescriptionPristine,
  isRunning,
  isTreatmentDescriptionPristine,
  isTreatmentPristine,
  requestingZeroRisk,
  updatingVulnerability,
}: IConfirmButtonsProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "api_mutations_request_vulnerabilities_zero_risk_mutate"
  );
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );
  const canUpdateVulnerabilityDescription: boolean = permissions.can(
    "api_mutations_update_vulnerability_description_mutate"
  );

  const { submitForm } = useFormikContext<IUpdateVulnerabilityForm>();

  return canRequestZeroRiskVuln ||
    canUpdateVulnsTreatment ||
    canUpdateVulnerabilityDescription ? (
    <ModalConfirm
      disabled={
        requestingZeroRisk ||
        updatingVulnerability ||
        deletingTag ||
        isRunning ||
        (isTreatmentDescriptionPristine &&
          isTreatmentPristine &&
          isDescriptionPristine)
      }
      onCancel={handleCloseModal}
      onConfirm={submitForm}
      txtCancel={t("group.findings.report.modalClose")}
    />
  ) : (
    <div />
  );
};

export { ConfirmButtons };

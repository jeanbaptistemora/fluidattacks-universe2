import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React, { useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";

import { PermanentlyAcceptedForm } from "./PermanentlyAcceptedForm";
import { SubmittedForm } from "./SubmittedForm";
import { getInitialTreatment } from "./utils";
import { ZeroRiskForm } from "./ZeroRiskForm";

import { FormikSelect } from "components/Input/Formik";
import { Modal } from "components/Modal";
import type { IHandleVulnerabilitiesAcceptanceModalProps } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/types";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

const HandleAcceptanceModal: React.FC<IHandleVulnerabilitiesAcceptanceModalProps> =
  ({
    findingId = undefined,
    groupName,
    vulns,
    handleCloseModal,
    refetchData,
  }: IHandleVulnerabilitiesAcceptanceModalProps): JSX.Element => {
    const { t } = useTranslation();
    const attributes: PureAbility<string> = useContext(authzGroupContext);
    const permissions: PureAbility<string> = useAbility(
      authzPermissionsContext
    );
    const canHandleVulnerabilitiesAcceptance: boolean = permissions.can(
      "api_mutations_handle_vulnerabilities_acceptance_mutate"
    );
    const canConfirmZeroRiskVulnerabilities: boolean = permissions.can(
      "api_mutations_confirm_vulnerabilities_zero_risk_mutate"
    );
    const canRejectZeroRiskVulnerabilities: boolean = permissions.can(
      "api_mutations_reject_vulnerabilities_zero_risk_mutate"
    );
    const canUpdateVulns: boolean = attributes.can(
      "can_report_vulnerabilities"
    );

    // State
    const [treatment, setTreatment] = useState(
      getInitialTreatment(
        canHandleVulnerabilitiesAcceptance,
        canConfirmZeroRiskVulnerabilities
      )
    );

    // Handle actions
    const handleTreatmentChange = useCallback(
      (event: React.ChangeEvent<HTMLSelectElement>): void => {
        setTreatment(event.target.value);
      },
      []
    );

    return (
      <React.StrictMode>
        <Modal
          onClose={handleCloseModal}
          open={true}
          title={t("searchFindings.tabDescription.handleAcceptanceModal.title")}
        >
          <FormikSelect
            field={{
              name: "treatment",
              onBlur: (): void => undefined,
              onChange: handleTreatmentChange,
              value: treatment,
            }}
            form={{ errors: {}, touched: {} }}
            label={t("searchFindings.tabDescription.treatment.title")}
            name={"treatment"}
          >
            <option value={""} />
            {canHandleVulnerabilitiesAcceptance ? (
              <option value={"ACCEPTED_UNDEFINED"}>
                {t("searchFindings.tabDescription.treatment.acceptedUndefined")}
              </option>
            ) : undefined}
            {canConfirmZeroRiskVulnerabilities &&
            canRejectZeroRiskVulnerabilities &&
            canUpdateVulns ? (
              <option value={"CONFIRM_REJECT_ZERO_RISK"}>
                {t(
                  "searchFindings.tabDescription.treatment.confirmRejectZeroRisk"
                )}
              </option>
            ) : undefined}
          </FormikSelect>
          <br />
          {treatment === "ACCEPTED_UNDEFINED" ? (
            <PermanentlyAcceptedForm
              findingId={findingId}
              onCancel={handleCloseModal}
              refetchData={refetchData}
              vulnerabilities={vulns}
            />
          ) : undefined}
          {treatment === "CONFIRM_REJECT_ZERO_RISK" ? (
            <ZeroRiskForm
              findingId={findingId}
              groupName={groupName}
              onCancel={handleCloseModal}
              refetchData={refetchData}
              vulnerabilities={vulns}
            />
          ) : undefined}
          {treatment === "CONFIRM_REJECT_VULNERABILITY" ? (
            <SubmittedForm
              findingId={findingId}
              groupName={groupName}
              onCancel={handleCloseModal}
              refetchData={refetchData}
              vulnerabilities={vulns}
            />
          ) : undefined}
        </Modal>
      </React.StrictMode>
    );
  };

export { HandleAcceptanceModal };

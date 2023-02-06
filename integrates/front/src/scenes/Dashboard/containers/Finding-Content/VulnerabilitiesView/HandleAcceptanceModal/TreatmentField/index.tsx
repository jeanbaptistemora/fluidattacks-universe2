import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React, { useContext } from "react";
import { useTranslation } from "react-i18next";

import { Select } from "components/Input";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { required } from "utils/validations";

const TreatmentField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const attributes: PureAbility<string> = useContext(authzGroupContext);
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canHandleVulnsAcceptance: boolean = permissions.can(
    "api_mutations_handle_vulnerabilities_acceptance_mutate"
  );
  const canConfirmZeroRiskVuln: boolean = permissions.can(
    "api_mutations_confirm_vulnerabilities_zero_risk_mutate"
  );
  const canRejectZeroRiskVuln: boolean = permissions.can(
    "api_mutations_reject_vulnerabilities_zero_risk_mutate"
  );
  const canUpdateVulns: boolean = attributes.can("can_report_vulnerabilities");

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("searchFindings.tabDescription.treatment.title")}</b>
      </ControlLabel>
      <Select name={"treatment"} validate={required}>
        <option value={""} />
        {canHandleVulnsAcceptance ? (
          <option value={"ACCEPTED_UNDEFINED"}>
            {t("searchFindings.tabDescription.treatment.acceptedUndefined")}
          </option>
        ) : undefined}
        {canConfirmZeroRiskVuln && canRejectZeroRiskVuln && canUpdateVulns ? (
          <option value={"CONFIRM_REJECT_ZERO_RISK"}>
            {t("searchFindings.tabDescription.treatment.confirmRejectZeroRisk")}
          </option>
        ) : undefined}
      </Select>
    </FormGroup>
  );
};

export { TreatmentField };

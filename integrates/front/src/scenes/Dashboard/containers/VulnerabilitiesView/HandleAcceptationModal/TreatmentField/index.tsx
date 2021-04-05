import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import { Field } from "redux-form";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { authzPermissionsContext } from "utils/authz/config";
import { Dropdown } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { required } from "utils/validations";

const TreatmentField: React.FC = (): JSX.Element => {
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canHandleVulnsAcceptation: boolean = permissions.can(
    "backend_api_mutations_handle_vulns_acceptation_mutate"
  );
  const canConfirmZeroRiskVuln: boolean = permissions.can(
    "backend_api_mutations_confirm_zero_risk_vuln_mutate"
  );
  const canRejectZeroRiskVuln: boolean = permissions.can(
    "backend_api_mutations_reject_zero_risk_vuln_mutate"
  );

  return (
    <FormGroup>
      <ControlLabel>
        <b>{translate.t("searchFindings.tabDescription.treatment.title")}</b>
      </ControlLabel>
      <Field
        component={Dropdown}
        name={"treatment"}
        type={"text"}
        validate={required}
      >
        <option value={""} />
        {canHandleVulnsAcceptation ? (
          <option value={"ACCEPTED_UNDEFINED"}>
            {translate.t(
              "searchFindings.tabDescription.treatment.acceptedUndefined"
            )}
          </option>
        ) : undefined}
        {canConfirmZeroRiskVuln ? (
          <option value={"CONFIRM_ZERO_RISK"}>
            {translate.t(
              "searchFindings.tabDescription.treatment.confirmZeroRisk"
            )}
          </option>
        ) : undefined}
        {canRejectZeroRiskVuln ? (
          <option value={"REJECT_ZERO_RISK"}>
            {translate.t(
              "searchFindings.tabDescription.treatment.rejectZeroRisk"
            )}
          </option>
        ) : undefined}
      </Field>
    </FormGroup>
  );
};

export { TreatmentField };

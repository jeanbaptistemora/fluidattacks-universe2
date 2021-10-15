import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Field } from "formik";
import React from "react";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { authzPermissionsContext } from "utils/authz/config";
import { FormikDropdown } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { required } from "utils/validations";

const TreatmentField: React.FC = (): JSX.Element => {
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

  return (
    <FormGroup>
      <ControlLabel>
        <b>{translate.t("searchFindings.tabDescription.treatment.title")}</b>
      </ControlLabel>
      <Field
        component={FormikDropdown}
        name={"treatment"}
        type={"text"}
        validate={required}
      >
        <option value={""} />
        {canHandleVulnsAcceptance ? (
          <option value={"ACCEPTED_UNDEFINED"}>
            {translate.t(
              "searchFindings.tabDescription.treatment.acceptedUndefined"
            )}
          </option>
        ) : undefined}
        {canConfirmZeroRiskVuln && canRejectZeroRiskVuln ? (
          <option value={"CONFIRM_REJECT_ZERO_RISK"}>
            {translate.t(
              "searchFindings.tabDescription.treatment.confirmRejectZeroRisk"
            )}
          </option>
        ) : undefined}
      </Field>
    </FormGroup>
  );
};

export { TreatmentField };

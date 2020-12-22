import { Dropdown } from "utils/forms/fields";
import { Field } from "redux-form";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { authzPermissionsContext } from "utils/authz/config";
import { required } from "utils/validations";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { ControlLabel, FormGroup } from "styles/styledComponents";

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
        <b>{translate.t("search_findings.tab_description.treatment.title")}</b>
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
              "search_findings.tab_description.treatment.accepted_undefined"
            )}
          </option>
        ) : undefined}
        {canConfirmZeroRiskVuln ? (
          <option value={"CONFIRM_ZERO_RISK"}>
            {translate.t(
              "search_findings.tab_description.treatment.confirm_zero_risk"
            )}
          </option>
        ) : undefined}
        {canRejectZeroRiskVuln ? (
          <option value={"REJECT_ZERO_RISK"}>
            {translate.t(
              "search_findings.tab_description.treatment.reject_zero_risk"
            )}
          </option>
        ) : undefined}
      </Field>
    </FormGroup>
  );
};

export { TreatmentField };

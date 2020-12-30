import type { ConfigurableValidator } from "revalidate";
import { Field } from "redux-form";
import type { IJustificationFieldProps } from "./types";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { authzPermissionsContext } from "utils/authz/config";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { Dropdown, TextArea } from "utils/forms/fields";
import { maxLength, required, validTextField } from "utils/validations";

const MAX_TREATMENT_JUSTIFICATION_LENGTH: number = 200;
const maxTreatmentJustificationLength: ConfigurableValidator = maxLength(
  MAX_TREATMENT_JUSTIFICATION_LENGTH
);
const JustificationField: React.FC<IJustificationFieldProps> = (
  props: IJustificationFieldProps
): JSX.Element => {
  const { isConfirmZeroRiskSelected, isRejectZeroRiskSelected } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canSeeDropDownToConfirmZeroRisk: boolean = permissions.can(
    "see_dropdown_to_confirm_zero_risk"
  );
  const canSeeDropDownToRejectZeroRisk: boolean = permissions.can(
    "see_dropdown_to_reject_zero_risk"
  );

  const shouldRenderDropdown: boolean =
    (canSeeDropDownToConfirmZeroRisk && isConfirmZeroRiskSelected) ||
    (canSeeDropDownToRejectZeroRisk && isRejectZeroRiskSelected);

  return (
    <FormGroup>
      <ControlLabel>
        <b>
          {translate.t(
            "search_findings.tab_description.remediation_modal.observations"
          )}
        </b>
      </ControlLabel>
      {shouldRenderDropdown ? (
        <Field
          component={Dropdown}
          name={"justification"}
          type={"text"}
          validate={required}
        >
          <option value={""} />
          {isConfirmZeroRiskSelected ? (
            <React.Fragment>
              <option value={"FP"}>
                {translate.t(
                  "search_findings.tab_description.handle_acceptation_modal.zero_risk_justification.confirmation.fp"
                )}
              </option>
              <option value={"Out of the scope"}>
                {translate.t(
                  "search_findings.tab_description.handle_acceptation_modal.zero_risk_justification.confirmation.out_of_the_scope"
                )}
              </option>
            </React.Fragment>
          ) : undefined}
          {isRejectZeroRiskSelected ? (
            <React.Fragment>
              <option value={"FN"}>
                {translate.t(
                  "search_findings.tab_description.handle_acceptation_modal.zero_risk_justification.rejection.fn"
                )}
              </option>
              <option value={"Complementary control"}>
                {translate.t(
                  "search_findings.tab_description.handle_acceptation_modal.zero_risk_justification.rejection.complementary_control"
                )}
              </option>
            </React.Fragment>
          ) : undefined}
        </Field>
      ) : (
        <Field
          component={TextArea}
          name={"justification"}
          type={"text"}
          validate={[required, validTextField, maxTreatmentJustificationLength]}
        />
      )}
    </FormGroup>
  );
};

export { JustificationField };

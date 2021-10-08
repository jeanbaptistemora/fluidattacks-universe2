import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Field } from "formik";
import React from "react";
import type { ConfigurableValidator } from "revalidate";

import type { IJustificationFieldProps } from "./types";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { authzPermissionsContext } from "utils/authz/config";
import { FormikDropdown, FormikTextArea } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  maxLength,
  required,
  validTextField,
} from "utils/validations";

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
            "searchFindings.tabDescription.remediationModal.observations"
          )}
        </b>
      </ControlLabel>
      {shouldRenderDropdown ? (
        <Field
          component={FormikDropdown}
          name={"justification"}
          type={"text"}
          validate={required}
        >
          <option value={""} />
          {isConfirmZeroRiskSelected ? (
            <React.Fragment>
              <option value={"FP"}>
                {translate.t(
                  "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.confirmation.fp"
                )}
              </option>
              <option value={"Out of the scope"}>
                {translate.t(
                  "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.confirmation.outOfTheScope"
                )}
              </option>
            </React.Fragment>
          ) : undefined}
          {isRejectZeroRiskSelected ? (
            <React.Fragment>
              <option value={"FN"}>
                {translate.t(
                  "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.rejection.fn"
                )}
              </option>
              <option value={"Complementary control"}>
                {translate.t(
                  "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.rejection.complementaryControl"
                )}
              </option>
            </React.Fragment>
          ) : undefined}
        </Field>
      ) : (
        <Field
          component={FormikTextArea}
          name={"justification"}
          type={"text"}
          validate={composeValidators([
            required,
            validTextField,
            maxTreatmentJustificationLength,
          ])}
        />
      )}
    </FormGroup>
  );
};

export { JustificationField };

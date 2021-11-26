import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import type { ConfigurableValidator } from "revalidate";

import type { IJustificationFieldProps } from "./types";

import { authzPermissionsContext } from "utils/authz/config";
import { EditableField, FormikTextArea } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  maxLength,
  required,
  validTextField,
} from "utils/validations";

const MAX_TREATMENT_JUSTIFICATION_LENGTH: number = 5000;
const maxTreatmentJustificationLength: ConfigurableValidator = maxLength(
  MAX_TREATMENT_JUSTIFICATION_LENGTH
);
const JustificationField: React.FC<IJustificationFieldProps> = (
  props: IJustificationFieldProps
): JSX.Element => {
  const { isTreatmentPristine, lastTreatment } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "api_mutations_request_vulnerabilities_zero_risk_mutate"
  );
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );

  return (
    <div className={"nt2 w-100"}>
      <EditableField
        component={FormikTextArea}
        currentValue={lastTreatment.justification as string}
        label={translate.t("searchFindings.tabDescription.treatmentJust")}
        name={"justification"}
        renderAsEditable={canUpdateVulnsTreatment || canRequestZeroRiskVuln}
        type={"text"}
        validate={
          isTreatmentPristine
            ? undefined
            : composeValidators([
                required,
                validTextField,
                maxTreatmentJustificationLength,
              ])
        }
      />
    </div>
  );
};

export { JustificationField };

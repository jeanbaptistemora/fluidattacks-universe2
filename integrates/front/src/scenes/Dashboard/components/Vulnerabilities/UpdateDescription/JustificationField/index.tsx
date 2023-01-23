import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import type { ConfigurableValidator } from "revalidate";

import type { IJustificationFieldProps } from "./types";

import { Editable, TextArea } from "components/Input";
import { authzPermissionsContext } from "utils/authz/config";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  maxLength,
  required,
  validTextField,
} from "utils/validations";

const MAX_TREATMENT_JUSTIFICATION_LENGTH: number = 10000;
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
      <Editable
        currentValue={lastTreatment.justification as string}
        isEditing={canUpdateVulnsTreatment || canRequestZeroRiskVuln}
        label={translate.t("searchFindings.tabDescription.treatmentJust")}
      >
        <TextArea
          label={translate.t("searchFindings.tabDescription.treatmentJust")}
          name={"justification"}
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
      </Editable>
    </div>
  );
};

export { JustificationField };

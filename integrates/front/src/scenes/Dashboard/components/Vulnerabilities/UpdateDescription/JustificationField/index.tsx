import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import type { ConfigurableValidator } from "revalidate";

import type { IJustificationFieldProps } from "./types";

import { EditableField } from "scenes/Dashboard/components/EditableField";
import { authzPermissionsContext } from "utils/authz/config";
import { TextArea } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { maxLength, required, validTextField } from "utils/validations";

const MAX_TREATMENT_JUSTIFICATION_LENGTH: number = 200;
const maxTreatmentJustificationLength: ConfigurableValidator = maxLength(
  MAX_TREATMENT_JUSTIFICATION_LENGTH
);
const JustificationField: React.FC<IJustificationFieldProps> = (
  props: IJustificationFieldProps
): JSX.Element => {
  const { isTreatmentPristine, lastTreatment } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "backend_api_mutations_request_zero_risk_vuln_mutate"
  );
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "backend_api_mutations_update_vulns_treatment_mutate"
  );

  return (
    <EditableField
      component={TextArea}
      currentValue={lastTreatment.justification as string}
      label={translate.t("searchFindings.tabDescription.treatmentJust")}
      name={"justification"}
      renderAsEditable={canUpdateVulnsTreatment || canRequestZeroRiskVuln}
      type={"text"}
      validate={
        isTreatmentPristine
          ? undefined
          : [required, validTextField, maxTreatmentJustificationLength]
      }
    />
  );
};

export { JustificationField };

import type { ConfigurableValidator } from "revalidate";
import { EditableField } from "scenes/Dashboard/components/EditableField";
import type { IJustificationFieldProps } from "./types";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { TextArea } from "utils/forms/fields";
import { authzPermissionsContext } from "utils/authz/config";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
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
      label={translate.t("search_findings.tab_description.treatmentJust")}
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

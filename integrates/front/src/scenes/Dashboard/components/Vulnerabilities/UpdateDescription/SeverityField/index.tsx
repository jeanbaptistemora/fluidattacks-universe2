import { EditableField } from "scenes/Dashboard/components/EditableField";
import { FormGroup } from "styles/styledComponents";
import type { ISeverityFieldProps } from "./types";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { Text } from "utils/forms/fields";
import { authzPermissionsContext } from "utils/authz/config";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { isValidVulnSeverity, numeric } from "utils/validations";

const SeverityField: React.FC<ISeverityFieldProps> = (
  props: ISeverityFieldProps
): JSX.Element => {
  const {
    hasNewVulnSelected,
    isAcceptedSelected,
    isAcceptedUndefinedSelected,
    isInProgressSelected,
    level,
  } = props;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "backend_api_mutations_update_vulns_treatment_mutate"
  );

  return (
    <React.StrictMode>
      {isAcceptedSelected ||
      isAcceptedUndefinedSelected ||
      isInProgressSelected ||
      !hasNewVulnSelected ? (
        <FormGroup>
          <EditableField
            component={Text}
            currentValue={level}
            label={translate.t(
              "search_findings.tabDescription.businessCriticality"
            )}
            name={"severity"}
            renderAsEditable={canUpdateVulnsTreatment}
            type={"number"}
            validate={[isValidVulnSeverity, numeric]}
          />
        </FormGroup>
      ) : undefined}
    </React.StrictMode>
  );
};

export { SeverityField };

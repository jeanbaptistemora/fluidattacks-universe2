import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";

import type { ISeverityFieldProps } from "./types";

import { authzPermissionsContext } from "utils/authz/config";
import { EditableField, FormikText } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  isValidVulnSeverity,
  numeric,
} from "utils/validations";

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
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );

  return (
    <React.StrictMode>
      {isAcceptedSelected ||
      isAcceptedUndefinedSelected ||
      isInProgressSelected ||
      !hasNewVulnSelected ? (
        <div className={"mb4 nt2 w-100"}>
          <EditableField
            component={FormikText}
            currentValue={level}
            label={translate.t(
              "searchFindings.tabDescription.businessCriticality"
            )}
            name={"severity"}
            renderAsEditable={canUpdateVulnsTreatment}
            type={"number"}
            validate={composeValidators([isValidVulnSeverity, numeric])}
          />
        </div>
      ) : undefined}
    </React.StrictMode>
  );
};

export { SeverityField };

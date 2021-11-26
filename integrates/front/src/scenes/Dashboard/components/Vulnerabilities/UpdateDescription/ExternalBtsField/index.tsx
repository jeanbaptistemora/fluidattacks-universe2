import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import type { ConfigurableValidator } from "revalidate";

import type { IExternalBtsFieldProps } from "./types";

import { groupExternalBugTrackingSystem } from "../utils";
import { authzPermissionsContext } from "utils/authz/config";
import { EditableField, FormikText } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { composeValidators, maxLength, validUrlField } from "utils/validations";

const MAX_BTS_LENGTH: number = 80;
const maxBtsLength: ConfigurableValidator = maxLength(MAX_BTS_LENGTH);

const ExternalBtsField: React.FC<IExternalBtsFieldProps> = (
  props: IExternalBtsFieldProps
): JSX.Element => {
  const {
    hasNewVulnSelected,
    isAcceptedSelected,
    isAcceptedUndefinedSelected,
    isInProgressSelected,
    vulnerabilities,
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
        <div className={"nt2 w-100"}>
          <EditableField
            component={FormikText}
            currentValue={groupExternalBugTrackingSystem(vulnerabilities)}
            label={translate.t("searchFindings.tabDescription.bts")}
            name={"externalBugTrackingSystem"}
            placeholder={translate.t(
              "searchFindings.tabDescription.btsPlaceholder"
            )}
            renderAsEditable={canUpdateVulnsTreatment}
            type={"text"}
            validate={composeValidators([maxBtsLength, validUrlField])}
          />
        </div>
      ) : undefined}
    </React.StrictMode>
  );
};

export { ExternalBtsField };

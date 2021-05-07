import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";
import type { ConfigurableValidator } from "revalidate";

import type { IExternalBtsFieldProps } from "./types";

import { groupExternalBts } from "../utils";
import { EditableField } from "scenes/Dashboard/components/EditableField";
import { authzPermissionsContext } from "utils/authz/config";
import { Text } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { maxLength, validUrlField } from "utils/validations";

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
    "api_mutations_update_vulns_treatment_mutate"
  );

  return (
    <React.StrictMode>
      {isAcceptedSelected ||
      isAcceptedUndefinedSelected ||
      isInProgressSelected ||
      !hasNewVulnSelected ? (
        <EditableField
          component={Text}
          currentValue={groupExternalBts(vulnerabilities)}
          label={translate.t("searchFindings.tabDescription.bts")}
          name={"externalBts"}
          placeholder={translate.t(
            "searchFindings.tabDescription.btsPlaceholder"
          )}
          renderAsEditable={canUpdateVulnsTreatment}
          type={"text"}
          validate={[maxBtsLength, validUrlField]}
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { ExternalBtsField };

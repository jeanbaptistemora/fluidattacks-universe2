import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import _ from "lodash";
import React from "react";

import type { IAssignedFieldProps } from "./types";

import { Editable, Select } from "components/Input";
import { authzPermissionsContext } from "utils/authz/config";
import { translate } from "utils/translations/translate";

const AssignedField: React.FC<IAssignedFieldProps> = ({
  isAcceptedSelected,
  isAcceptedUndefinedSelected,
  isInProgressSelected,
  lastTreatment,
  userEmails,
}: IAssignedFieldProps): JSX.Element => {
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );

  return (
    <React.StrictMode>
      {isInProgressSelected ||
      isAcceptedSelected ||
      isAcceptedUndefinedSelected ? (
        <Editable
          currentValue={_.get(lastTreatment, "assigned", "")}
          isEditing={canUpdateVulnsTreatment}
          label={translate.t("searchFindings.tabDescription.assigned")}
        >
          <Select
            label={translate.t("searchFindings.tabDescription.assigned")}
            name={"assigned"}
          >
            {userEmails.map(
              (email: string): JSX.Element => (
                <option key={email} value={email}>
                  {email}
                </option>
              )
            )}
          </Select>
        </Editable>
      ) : undefined}
    </React.StrictMode>
  );
};

export { AssignedField };

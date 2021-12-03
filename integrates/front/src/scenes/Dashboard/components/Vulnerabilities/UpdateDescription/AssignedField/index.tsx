import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import _ from "lodash";
import React from "react";

import type { IAssignedFieldProps } from "./types";

import { authzPermissionsContext } from "utils/authz/config";
import { EditableField, FormikDropdown } from "utils/forms/fields";
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
        <EditableField
          component={FormikDropdown}
          currentValue={_.get(lastTreatment, "assigned", "")}
          label={translate.t("searchFindings.tabDescription.assigned")}
          name={"assigned"}
          renderAsEditable={canUpdateVulnsTreatment}
          type={"text"}
        >
          <option value={""} />
          {userEmails.map(
            (email: string): JSX.Element => (
              <option key={email} value={email}>
                {email}
              </option>
            )
          )}
        </EditableField>
      ) : undefined}
    </React.StrictMode>
  );
};

export { AssignedField };

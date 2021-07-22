import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import _ from "lodash";
import React from "react";

import type { ITreatmentManagerFieldProps } from "./types";

import { authzPermissionsContext } from "utils/authz/config";
import { EditableField, FormikDropdown } from "utils/forms/fields";
import { translate } from "utils/translations/translate";

const TreatmentManagerField: React.FC<ITreatmentManagerFieldProps> = (
  props: ITreatmentManagerFieldProps
): JSX.Element => {
  const { isInProgressSelected, lastTreatment, userEmails } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );

  return (
    <React.StrictMode>
      {isInProgressSelected ? (
        <EditableField
          component={FormikDropdown}
          currentValue={_.get(lastTreatment, "treatmentManager", "")}
          label={translate.t("searchFindings.tabDescription.treatmentMgr")}
          name={"treatmentManager"}
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

export { TreatmentManagerField };

import { Dropdown } from "utils/forms/fields";
import { EditableField } from "scenes/Dashboard/components/EditableField";
import type { ITreatmentManagerFieldProps } from "./types";
import type { PureAbility } from "@casl/ability";
import React from "react";
import _ from "lodash";
import { authzPermissionsContext } from "utils/authz/config";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";

const TreatmentManagerField: React.FC<ITreatmentManagerFieldProps> = (
  props: ITreatmentManagerFieldProps
): JSX.Element => {
  const { isInProgressSelected, lastTreatment, userEmails } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "backend_api_mutations_update_vulns_treatment_mutate"
  );

  return (
    <React.StrictMode>
      {isInProgressSelected ? (
        <EditableField
          component={Dropdown}
          currentValue={_.get(lastTreatment, "treatmentManager", "")}
          label={translate.t("search_findings.tabDescription.treatmentMgr")}
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

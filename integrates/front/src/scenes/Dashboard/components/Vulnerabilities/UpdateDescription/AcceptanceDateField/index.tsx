import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import _ from "lodash";
import React from "react";

import type { IAcceptanceDateFieldProps } from "./types";

import { EditableField } from "scenes/Dashboard/components/EditableField";
import { authzPermissionsContext } from "utils/authz/config";
import { Date } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { isLowerDate, required } from "utils/validations";

const AcceptanceDateField: React.FC<IAcceptanceDateFieldProps> = (
  props: IAcceptanceDateFieldProps
): JSX.Element => {
  const { isAcceptedSelected, lastTreatment } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "backend_api_mutations_update_vulns_treatment_mutate"
  );

  return (
    <React.StrictMode>
      {isAcceptedSelected ? (
        <EditableField
          component={Date}
          currentValue={_.get(lastTreatment, "acceptanceDate", "-")}
          label={translate.t("searchFindings.tabDescription.acceptanceDate")}
          name={"acceptanceDate"}
          renderAsEditable={canUpdateVulnsTreatment}
          type={"date"}
          validate={[required, isLowerDate]}
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { AcceptanceDateField };

import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import _ from "lodash";
import React from "react";

import type { IAcceptanceDateFieldProps } from "./types";

import { authzPermissionsContext } from "utils/authz/config";
import { EditableField, FormikDate } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { composeValidators, isLowerDate, required } from "utils/validations";

const AcceptanceDateField: React.FC<IAcceptanceDateFieldProps> = (
  props: IAcceptanceDateFieldProps
): JSX.Element => {
  const { isAcceptedSelected, lastTreatment } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );

  return (
    <React.StrictMode>
      {isAcceptedSelected ? (
        <div className={"nt2 w-100"}>
          <EditableField
            component={FormikDate}
            currentValue={_.get(lastTreatment, "acceptanceDate", "-")}
            label={translate.t("searchFindings.tabDescription.acceptanceDate")}
            name={"acceptanceDate"}
            renderAsEditable={canUpdateVulnsTreatment}
            type={"date"}
            validate={composeValidators([required, isLowerDate])}
          />
        </div>
      ) : undefined}
    </React.StrictMode>
  );
};

export { AcceptanceDateField };

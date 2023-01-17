import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IAcceptanceDateFieldProps } from "./types";

import { Editable, InputDate } from "components/Input";
import { authzPermissionsContext } from "utils/authz/config";
import { composeValidators, isLowerDate, required } from "utils/validations";

const AcceptanceDateField: React.FC<IAcceptanceDateFieldProps> = ({
  isAcceptedSelected,
  lastTreatment,
}): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );

  return (
    <React.StrictMode>
      {isAcceptedSelected ? (
        <div className={"mb4 nt2 w-100"}>
          <Editable
            currentValue={_.get(lastTreatment, "acceptanceDate", "-")}
            isEditing={canUpdateVulnsTreatment}
            label={t("searchFindings.tabDescription.acceptanceDate")}
          >
            <InputDate
              label={t("searchFindings.tabDescription.acceptanceDate")}
              name={"acceptanceDate"}
              validate={composeValidators([required, isLowerDate])}
            />
          </Editable>
        </div>
      ) : undefined}
    </React.StrictMode>
  );
};

export { AcceptanceDateField };

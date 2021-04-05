import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React from "react";

import type { ITreatmentFieldProps } from "./types";

import { EditableField } from "scenes/Dashboard/components/EditableField";
import { authzPermissionsContext } from "utils/authz/config";
import { formatDropdownField } from "utils/formatHelpers";
import { Dropdown } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { required } from "utils/validations";

const TreatmentField: React.FC<ITreatmentFieldProps> = (
  props: ITreatmentFieldProps
): JSX.Element => {
  const { isTreatmentPristine, lastTreatment } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "backend_api_mutations_request_zero_risk_vuln_mutate"
  );
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "backend_api_mutations_update_vulns_treatment_mutate"
  );

  const isAcceptedUndefinedPendingToApproved: boolean =
    lastTreatment.treatment === "ACCEPTED_UNDEFINED" &&
    lastTreatment.acceptanceStatus !== "APPROVED";
  const treatmentLabel: string =
    translate.t(formatDropdownField(lastTreatment.treatment)) +
    (isAcceptedUndefinedPendingToApproved
      ? translate.t("searchFindings.tabDescription.treatment.pendingApproval")
      : "");

  return (
    <EditableField
      component={Dropdown}
      currentValue={treatmentLabel}
      label={translate.t("searchFindings.tabDescription.treatment.title")}
      name={"treatment"}
      renderAsEditable={canUpdateVulnsTreatment || canRequestZeroRiskVuln}
      type={"text"}
      validate={isTreatmentPristine ? [] : required}
    >
      <option value={""} />
      {canUpdateVulnsTreatment ? (
        <React.Fragment>
          <option value={"IN_PROGRESS"}>
            {translate.t("searchFindings.tabDescription.treatment.inProgress")}
          </option>
          <option value={"ACCEPTED"}>
            {translate.t("searchFindings.tabDescription.treatment.accepted")}
          </option>
          <option value={"ACCEPTED_UNDEFINED"}>
            {translate.t(
              "searchFindings.tabDescription.treatment.acceptedUndefined"
            )}
          </option>
        </React.Fragment>
      ) : undefined}
      {canRequestZeroRiskVuln ? (
        <option value={"REQUEST_ZERO_RISK"}>
          {translate.t(
            "searchFindings.tabDescription.treatment.requestZeroRisk"
          )}
        </option>
      ) : undefined}
    </EditableField>
  );
};

export { TreatmentField };

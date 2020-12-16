import { Dropdown } from "utils/forms/fields";
import { EditableField } from "scenes/Dashboard/components/EditableField";
import type { ITreatmentFieldProps } from "./types";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { authzPermissionsContext } from "utils/authz/config";
import { formatDropdownField } from "utils/formatHelpers";
import { required } from "utils/validations";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";

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
      ? translate.t(
          "search_findings.tab_description.treatment.pending_approval"
        )
      : "");

  return (
    <EditableField
      component={Dropdown}
      currentValue={treatmentLabel}
      label={translate.t("search_findings.tab_description.treatment.title")}
      name={"treatment"}
      renderAsEditable={canUpdateVulnsTreatment || canRequestZeroRiskVuln}
      type={"text"}
      validate={isTreatmentPristine ? [] : required}
    >
      <option value={""} />
      {canUpdateVulnsTreatment ? (
        <React.Fragment>
          <option value={"IN_PROGRESS"}>
            {translate.t(
              "search_findings.tab_description.treatment.in_progress"
            )}
          </option>
          <option value={"ACCEPTED"}>
            {translate.t("search_findings.tab_description.treatment.accepted")}
          </option>
          <option value={"ACCEPTED_UNDEFINED"}>
            {translate.t(
              "search_findings.tab_description.treatment.accepted_undefined"
            )}
          </option>
        </React.Fragment>
      ) : undefined}
      {canRequestZeroRiskVuln ? (
        <option value={"REQUEST_ZERO_RISK"}>
          {translate.t(
            "search_findings.tab_description.treatment.request_zero_risk"
          )}
        </option>
      ) : undefined}
    </EditableField>
  );
};

export { TreatmentField };

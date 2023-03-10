import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React, { useContext } from "react";
import { useTranslation } from "react-i18next";

import type { ITreatmentFieldProps } from "./types";

import { Editable, Select } from "components/Input";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { formatDropdownField } from "utils/formatHelpers";
import { required } from "utils/validations";

const TreatmentField: React.FC<ITreatmentFieldProps> = ({
  areSelectedSubmittedVulnerabilities,
  isTreatmentPristine,
  lastTreatment,
}: ITreatmentFieldProps): JSX.Element => {
  const { t } = useTranslation();

  const attributes: PureAbility<string> = useContext(authzGroupContext);
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRequestZeroRiskVuln: boolean =
    permissions.can("api_mutations_request_vulnerabilities_zero_risk_mutate") &&
    attributes.can("can_report_vulnerabilities") &&
    !areSelectedSubmittedVulnerabilities;
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );

  const isAcceptedUndefinedPendingToApproved: boolean =
    lastTreatment.treatment === "ACCEPTED_UNDEFINED" &&
    lastTreatment.acceptanceStatus !== "APPROVED";
  const treatmentLabel: string =
    t(formatDropdownField(lastTreatment.treatment)) +
    (isAcceptedUndefinedPendingToApproved
      ? t("searchFindings.tabDescription.treatment.pendingApproval")
      : "");

  return (
    <Editable
      currentValue={treatmentLabel}
      isEditing={canUpdateVulnsTreatment || canRequestZeroRiskVuln}
      label={t("searchFindings.tabDescription.treatment.title")}
    >
      <Select
        label={t("searchFindings.tabDescription.treatment.title")}
        name={"treatment"}
        validate={isTreatmentPristine ? undefined : required}
      >
        <option value={""}>
          {t("searchFindings.tabDescription.treatment.new")}
        </option>
        {canUpdateVulnsTreatment ? (
          <React.Fragment>
            <option value={"IN_PROGRESS"}>
              {t("searchFindings.tabDescription.treatment.inProgress")}
            </option>
            <option value={"ACCEPTED"}>
              {t("searchFindings.tabDescription.treatment.accepted")}
            </option>
            <option value={"ACCEPTED_UNDEFINED"}>
              {t("searchFindings.tabDescription.treatment.acceptedUndefined")}
            </option>
          </React.Fragment>
        ) : undefined}
        {canRequestZeroRiskVuln ? (
          <option value={"REQUEST_ZERO_RISK"}>
            {t("searchFindings.tabDescription.treatment.requestZeroRisk")}
          </option>
        ) : undefined}
      </Select>
    </Editable>
  );
};

export { TreatmentField };

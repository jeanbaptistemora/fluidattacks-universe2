import React from "react";

import type { IAcceptanceUserFieldProps } from "./types";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

const AcceptanceUserField: React.FC<IAcceptanceUserFieldProps> = (
  props: IAcceptanceUserFieldProps
): JSX.Element => {
  const {
    isAcceptedSelected,
    isAcceptedUndefinedSelected,
    isInProgressSelected,
    lastTreatment,
  } = props;

  const isLastTreatmentAcceptanceStatusApproved: boolean =
    lastTreatment.acceptanceStatus === "APPROVED";

  return (
    <React.StrictMode>
      {(isAcceptedSelected ||
        isAcceptedUndefinedSelected ||
        isInProgressSelected) &&
      isLastTreatmentAcceptanceStatusApproved ? (
        <FormGroup>
          <ControlLabel>
            <b>{translate.t("searchFindings.tabDescription.acceptanceUser")}</b>
          </ControlLabel>
          <p>{lastTreatment.user}</p>
        </FormGroup>
      ) : undefined}
    </React.StrictMode>
  );
};

export { AcceptanceUserField };

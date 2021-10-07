import React from "react";

import type { IAcceptationUserFieldProps } from "./types";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

const AcceptationUserField: React.FC<IAcceptationUserFieldProps> = (
  props: IAcceptationUserFieldProps
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

export { AcceptationUserField };

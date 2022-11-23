import React from "react";

import type { IAcceptanceUserFieldProps } from "./types";

import { ControlLabel } from "styles/styledComponents";
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
        <div className={"mb4 nt2 w-100"}>
          <ControlLabel>
            <b>{translate.t("searchFindings.tabDescription.acceptanceUser")}</b>
          </ControlLabel>
          <p>{lastTreatment.user}</p>
        </div>
      ) : undefined}
    </React.StrictMode>
  );
};

export { AcceptanceUserField };

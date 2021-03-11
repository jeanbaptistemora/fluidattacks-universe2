import type { IAcceptationUserFieldProps } from "./types";
import React from "react";
import { translate } from "utils/translations/translate";
import { ControlLabel, FormGroup } from "styles/styledComponents";

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
            <b>
              {translate.t("search_findings.tabDescription.acceptationUser")}
            </b>
          </ControlLabel>
          <p>{lastTreatment.user}</p>
        </FormGroup>
      ) : undefined}
    </React.StrictMode>
  );
};

export { AcceptationUserField };

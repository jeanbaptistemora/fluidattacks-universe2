import type { IAcceptationUserFieldProps } from "./types";
import React from "react";
import { translate } from "utils/translations/translate";
import { ControlLabel, FormGroup } from "react-bootstrap/lib";

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
              {translate.t("search_findings.tab_description.acceptation_user")}
            </b>
          </ControlLabel>
          <p>{lastTreatment.user}</p>
        </FormGroup>
      ) : undefined}
    </React.StrictMode>
  );
};

export { AcceptationUserField };

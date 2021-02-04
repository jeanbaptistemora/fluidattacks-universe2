import { Field } from "redux-form";
import type { ISeverityFieldProps } from "./types";
import React from "react";
import { Text } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { isValidVulnSeverity, numeric } from "utils/validations";

const SeverityField: React.FC<ISeverityFieldProps> = (
  props: ISeverityFieldProps
): JSX.Element => {
  const {
    isAcceptedSelected,
    isAcceptedUndefinedSelected,
    isInProgressSelected,
  } = props;

  return (
    <React.StrictMode>
      {isAcceptedSelected ||
      isAcceptedUndefinedSelected ||
      isInProgressSelected ? (
        <FormGroup>
          <ControlLabel>
            <b>
              {translate.t(
                "search_findings.tab_description.business_criticality"
              )}
            </b>
          </ControlLabel>
          <Field
            component={Text}
            name={"severity"}
            type={"number"}
            validate={[isValidVulnSeverity, numeric]}
          />
        </FormGroup>
      ) : undefined}
    </React.StrictMode>
  );
};

export { SeverityField };

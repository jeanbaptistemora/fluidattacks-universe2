import type { ConfigurableValidator } from "revalidate";
import { Field } from "redux-form";
import React from "react";
import { TextArea } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { maxLength, required, validTextField } from "utils/validations";

const MAX_TREATMENT_JUSTIFICATION_LENGTH: number = 200;
const maxTreatmentJustificationLength: ConfigurableValidator = maxLength(
  MAX_TREATMENT_JUSTIFICATION_LENGTH
);
const JustificationField: React.FC = (): JSX.Element => {
  return (
    <FormGroup>
      <ControlLabel>
        <b>
          {translate.t(
            "search_findings.tab_description.remediation_modal.observations"
          )}
        </b>
      </ControlLabel>
      <Field
        component={TextArea}
        name={"justification"}
        type={"text"}
        validate={[required, validTextField, maxTreatmentJustificationLength]}
      />
    </FormGroup>
  );
};

export { JustificationField };

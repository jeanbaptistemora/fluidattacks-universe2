import { Field } from "formik";
import React from "react";

import type { ISeenFirstTimeByFieldProps } from "./types";

import type { IStakeholderAttr } from "../types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikDropdown } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { required } from "utils/validations";

const SeenFirstTimeByField: React.FC<ISeenFirstTimeByFieldProps> = (
  props: ISeenFirstTimeByFieldProps
): JSX.Element => {
  const { validStakeholders } = props;

  return (
    <FormGroup>
      <ControlLabel>
        <b>
          {translate.t(
            "group.toe.inputs.enumerateModal.fields.seenFirstTimeBy"
          )}
        </b>
      </ControlLabel>
      <Field
        component={FormikDropdown}
        name={"seenFirstTimeBy"}
        type={"text"}
        validate={required}
      >
        <option value={""} />
        {validStakeholders.map(
          (stakeholder: IStakeholderAttr): JSX.Element => (
            <option key={stakeholder.email} value={stakeholder.email}>
              {stakeholder.email}
            </option>
          )
        )}
      </Field>
    </FormGroup>
  );
};

export { SeenFirstTimeByField };

import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikDateTime } from "utils/forms/fields";
import {
  composeValidators,
  dateTimeBeforeToday,
  required,
} from "utils/validations";

const ModifiedDateField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("group.toe.lines.addModal.fields.modifiedDate")} </b>
      </ControlLabel>
      <Field
        component={FormikDateTime}
        name={"modifiedDate"}
        type={"text"}
        validate={composeValidators([required, dateTimeBeforeToday])}
      />
    </FormGroup>
  );
};

export { ModifiedDateField };

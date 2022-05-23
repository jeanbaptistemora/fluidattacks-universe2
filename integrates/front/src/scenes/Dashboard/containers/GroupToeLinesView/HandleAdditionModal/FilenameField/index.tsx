import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikTextArea } from "utils/forms/fields";
import {
  composeValidators,
  required,
  validCsvInput,
  validTextField,
} from "utils/validations";

const FilenameField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("group.toe.lines.addModal.fields.filename")} </b>
      </ControlLabel>
      <Field
        component={FormikTextArea}
        name={"filename"}
        type={"text"}
        validate={composeValidators([required, validCsvInput, validTextField])}
      />
    </FormGroup>
  );
};

export { FilenameField };

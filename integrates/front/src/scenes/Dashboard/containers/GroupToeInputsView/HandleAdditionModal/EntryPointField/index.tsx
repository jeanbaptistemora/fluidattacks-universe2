import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import { composeValidators, validTextField } from "utils/validations";

const EntryPointField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("group.toe.inputs.addModal.fields.entryPoint")} </b>
      </ControlLabel>
      <Field
        component={FormikText}
        name={"entryPoint"}
        type={"text"}
        validate={composeValidators([validTextField])}
      />
    </FormGroup>
  );
};

export { EntryPointField };

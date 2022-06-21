import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IPasswordFieldProps } from "./types";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import { composeValidators, required } from "utils/validations";

const PasswordField: React.FC<IPasswordFieldProps> = (
  props: IPasswordFieldProps
): JSX.Element => {
  const { disabled } = props;
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>{t("profile.credentialsModal.form.password")}</ControlLabel>
      <Field
        component={FormikText}
        disabled={disabled}
        name={"password"}
        type={"text"}
        validate={composeValidators([required])}
      />
    </FormGroup>
  );
};

export { PasswordField };

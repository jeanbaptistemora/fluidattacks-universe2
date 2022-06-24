import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IUserFieldProps } from "./types";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import { composeValidators, required } from "utils/validations";

const UserField: React.FC<IUserFieldProps> = (
  props: IUserFieldProps
): JSX.Element => {
  const { disabled } = props;
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>{t("profile.credentialsModal.form.user")}</ControlLabel>
      <Field
        component={FormikText}
        disabled={disabled}
        name={"user"}
        type={"text"}
        validate={composeValidators([required])}
      />
    </FormGroup>
  );
};

export { UserField };

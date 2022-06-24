import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import type { INameFieldProps } from "./types";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import { composeValidators, required } from "utils/validations";

const NameField: React.FC<INameFieldProps> = (
  props: INameFieldProps
): JSX.Element => {
  const { disabled } = props;
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        {t("profile.credentialsModal.form.name.label")}
      </ControlLabel>
      <Field
        component={FormikText}
        disabled={disabled}
        name={"name"}
        placeholder={t("profile.credentialsModal.form.name.placeholder")}
        type={"text"}
        validate={composeValidators([required])}
      />
    </FormGroup>
  );
};

export { NameField };

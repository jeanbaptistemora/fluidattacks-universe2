import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import type { ITokenFieldProps } from "./types";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import { composeValidators, required } from "utils/validations";

const TokenField: React.FC<ITokenFieldProps> = (
  props: ITokenFieldProps
): JSX.Element => {
  const { disabled } = props;
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>{t("profile.credentialsModal.form.token")}</ControlLabel>
      <Field
        component={FormikText}
        disabled={disabled}
        name={"accessToken"}
        type={"text"}
        validate={composeValidators([required])}
      />
    </FormGroup>
  );
};

export { TokenField };

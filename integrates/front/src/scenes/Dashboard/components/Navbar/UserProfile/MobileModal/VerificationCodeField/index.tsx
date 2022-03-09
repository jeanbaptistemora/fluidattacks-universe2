import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IVerificationCodeFieldProps } from "./types";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import { composeValidators, required } from "utils/validations";

const VerificationCodeField: React.FC<IVerificationCodeFieldProps> = (
  props: IVerificationCodeFieldProps
): JSX.Element => {
  const { disabled } = props;
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("profile.mobileModal.fields.verificationCode")}</b>
      </ControlLabel>
      <Field
        component={FormikText}
        disabled={disabled}
        name={"verificationCode"}
        type={"text"}
        validate={composeValidators([required])}
      />
    </FormGroup>
  );
};

export { VerificationCodeField };

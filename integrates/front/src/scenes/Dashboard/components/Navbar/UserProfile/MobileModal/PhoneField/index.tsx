import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IPhoneFieldProps } from "./types";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikPhone } from "utils/forms/fields/PhoneNumber/FormikPhone";
import { composeValidators, required } from "utils/validations";

const PhoneField: React.FC<IPhoneFieldProps> = (
  props: IPhoneFieldProps
): JSX.Element => {
  const { autoFocus, disabled } = props;
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("profile.mobileModal.fields.number")}</b>
      </ControlLabel>
      <Field
        // eslint-disable-next-line jsx-a11y/no-autofocus
        autoFocus={autoFocus}
        component={FormikPhone}
        disabled={disabled}
        name={"phone"}
        validate={composeValidators([required])}
      />
    </FormGroup>
  );
};

export { PhoneField };

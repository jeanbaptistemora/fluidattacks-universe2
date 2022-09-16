/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
import { Field } from "formik";
import React from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

import { Label } from "components/Input";
import { FormikPhone } from "utils/forms/fields/PhoneNumber/FormikPhone";
import {
  composeValidators,
  isValidPhoneNumber,
  required,
} from "utils/validations";

interface IPhoneFieldProps {
  autoFocus?: boolean;
  disabled?: boolean;
  label?: string;
  name?: string;
}

const PhoneField: FC<IPhoneFieldProps> = ({
  autoFocus,
  disabled,
  label,
  name,
}: Readonly<IPhoneFieldProps>): JSX.Element => {
  const { t } = useTranslation();

  return (
    <div>
      <Label>{t(label ?? "profile.mobileModal.fields.phoneNumber")}</Label>
      <Field
        // eslint-disable-next-line jsx-a11y/no-autofocus
        autoFocus={autoFocus}
        component={FormikPhone}
        disabled={disabled}
        name={name ?? "phone"}
        validate={composeValidators([required, isValidPhoneNumber])}
      />
    </div>
  );
};

export { PhoneField };

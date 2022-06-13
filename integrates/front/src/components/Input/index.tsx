import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputProps } from "./CustomInput";
import { CustomInput } from "./CustomInput";

const Input: FC<IInputProps> = ({
  alertType,
  customBlur,
  customKeyDown,
  disabled,
  name,
  placeholder,
  type,
  variant,
}: Readonly<IInputProps>): JSX.Element => (
  <Field
    alertType={alertType}
    component={CustomInput}
    customBlur={customBlur}
    customKeyDown={customKeyDown}
    disabled={disabled}
    name={name}
    placeholder={placeholder}
    type={type}
    variant={variant}
  />
);

export { Input };

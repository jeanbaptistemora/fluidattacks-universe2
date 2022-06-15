import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputProps } from "./CustomInput";
import { CustomInput } from "./CustomInput";

const Input: FC<IInputProps> = ({
  alertType,
  onBlur,
  onFocus,
  onKeyDown,
  disabled,
  name,
  placeholder,
  type,
  variant,
}: Readonly<IInputProps>): JSX.Element => (
  <Field
    alertType={alertType}
    component={CustomInput}
    disabled={disabled}
    name={name}
    onBlur={onBlur}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    placeholder={placeholder}
    type={type}
    variant={variant}
  />
);

export { Input };

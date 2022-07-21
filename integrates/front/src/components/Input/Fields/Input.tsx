import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputProps } from "../Formik";
import { FormikInput } from "../Formik";

const Input: FC<IInputProps> = ({
  childLeft,
  childRight,
  disabled = false,
  id,
  label,
  name,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
  type = "text",
  variant = "solid",
}: Readonly<IInputProps>): JSX.Element => (
  <Field
    childLeft={childLeft}
    childRight={childRight}
    component={FormikInput}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    onBlur={onBlur}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    placeholder={placeholder}
    required={required}
    tooltip={tooltip}
    type={type}
    variant={variant}
  />
);

export { Input };

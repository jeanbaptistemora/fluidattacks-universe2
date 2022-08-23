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
  list,
  name,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
  type = "text",
  validate,
  variant = "solid",
}: Readonly<IInputProps>): JSX.Element => (
  <Field
    childLeft={childLeft}
    childRight={childRight}
    component={FormikInput}
    disabled={disabled}
    id={id}
    label={label}
    list={list}
    name={name}
    onBlur={onBlur}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    placeholder={placeholder}
    required={required}
    tooltip={tooltip}
    type={type}
    validate={validate}
    variant={variant}
  />
);

export { Input };

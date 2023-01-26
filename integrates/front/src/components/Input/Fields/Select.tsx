import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { ISelectProps } from "../Formik/FormikSelect";
import { FormikSelect } from "../Formik/FormikSelect";

const Select: FC<ISelectProps> = ({
  children,
  disabled,
  id,
  label,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
  validate,
  variant,
}: Readonly<ISelectProps>): JSX.Element => (
  <Field
    component={FormikSelect}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    onBlur={onBlur}
    onChange={onChange}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    placeholder={placeholder}
    required={required}
    tooltip={tooltip}
    type={"text"}
    validate={validate}
    variant={variant}
  >
    {children}
  </Field>
);

export { Select };

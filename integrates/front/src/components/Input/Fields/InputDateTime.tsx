import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputDateTimeProps } from "../Formik/FormikDateTime";
import { FormikDateTime } from "../Formik/FormikDateTime";

const InputDateTime: FC<IInputDateTimeProps> = ({
  disabled = false,
  id,
  label,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  required,
  tooltip,
  variant = "solid",
}: Readonly<IInputDateTimeProps>): JSX.Element => (
  <Field
    component={FormikDateTime}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    onBlur={onBlur}
    onChange={onChange}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    required={required}
    tooltip={tooltip}
    variant={variant}
  />
);

export { InputDateTime };

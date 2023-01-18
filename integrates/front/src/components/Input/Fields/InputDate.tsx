import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputDateProps } from "../Formik/FormikDate";
import { FormikDate } from "../Formik/FormikDate";

const InputDate: FC<IInputDateProps> = ({
  disabled = false,
  id,
  label,
  max,
  min,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  required,
  tooltip,
  validate,
  variant = "solid",
}: Readonly<IInputDateProps>): JSX.Element => (
  <Field
    component={FormikDate}
    disabled={disabled}
    id={id}
    label={label}
    max={max}
    min={min}
    name={name}
    onBlur={onBlur}
    onChange={onChange}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    required={required}
    tooltip={tooltip}
    validate={validate}
    variant={variant}
  />
);

export { InputDate };

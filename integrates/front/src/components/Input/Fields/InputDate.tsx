import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputDateProps } from "../Formik";
import { FormikDate } from "../Formik";

const InputDate: FC<IInputDateProps> = ({
  disabled = false,
  id,
  label,
  max,
  min,
  name,
  onBlur,
  onFocus,
  onKeyDown,
  required,
  tooltip,
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
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    required={required}
    tooltip={tooltip}
    variant={variant}
  />
);

export { InputDate };

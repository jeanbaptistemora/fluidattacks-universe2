import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputNumberProps } from "../Formik/FormikNumber";
import { FormikNumber } from "../Formik/FormikNumber";

const InputNumber: FC<IInputNumberProps> = ({
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
  placeholder,
  required,
  tooltip,
  variant = "solid",
}: Readonly<IInputNumberProps>): JSX.Element => (
  <Field
    component={FormikNumber}
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
    placeholder={placeholder}
    required={required}
    tooltip={tooltip}
    variant={variant}
  />
);

export { InputNumber };

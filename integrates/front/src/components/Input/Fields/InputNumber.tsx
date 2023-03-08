import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputNumberProps } from "../Formik/FormikNumber";
import { FormikNumber } from "../Formik/FormikNumber";

const InputNumber: FC<IInputNumberProps> = ({
  decimalPlaces = 0,
  disabled,
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
  validate,
  variant,
}: Readonly<IInputNumberProps>): JSX.Element => (
  <Field
    component={FormikNumber}
    decimalPlaces={decimalPlaces}
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
    validate={validate}
    variant={variant}
  />
);

export { InputNumber };

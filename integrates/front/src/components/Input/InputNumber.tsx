import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputNumberProps } from "./FormikInputNumber";
import { FormikInputNumber } from "./FormikInputNumber";

const InputNumber: FC<IInputNumberProps> = ({
  disabled = false,
  id,
  label,
  max,
  min,
  name,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  tooltip,
  variant = "solid",
}: Readonly<IInputNumberProps>): JSX.Element => (
  <Field
    component={FormikInputNumber}
    disabled={disabled}
    id={id}
    label={label}
    max={max}
    min={min}
    name={name}
    onBlur={onBlur}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    placeholder={placeholder}
    tooltip={tooltip}
    variant={variant}
  />
);

export type { IInputNumberProps };
export { InputNumber };

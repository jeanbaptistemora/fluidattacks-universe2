import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { ICheckboxProps } from "../Formik/FormikCheckbox";
import { FormikCheckbox } from "../Formik/FormikCheckbox";

const Checkbox: FC<ICheckboxProps> = ({
  disabled,
  id,
  label,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  required,
  tooltip,
  validate,
  value,
}: Readonly<ICheckboxProps>): JSX.Element => (
  <Field
    component={FormikCheckbox}
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
    type={"checkbox"}
    validate={validate}
    value={value}
  />
);

export type { ICheckboxProps };
export { Checkbox };

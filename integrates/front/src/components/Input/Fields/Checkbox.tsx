import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { ICheckboxProps } from "../Formik";
import { FormikCheckbox } from "../Formik";

const Checkbox: FC<ICheckboxProps> = ({
  checked,
  disabled,
  id,
  label,
  name,
  required,
  tooltip,
  value,
}: Readonly<ICheckboxProps>): JSX.Element => (
  <Field
    checked={checked}
    component={FormikCheckbox}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    required={required}
    tooltip={tooltip}
    type={"checkbox"}
    value={value}
  />
);

export type { ICheckboxProps };
export { Checkbox };

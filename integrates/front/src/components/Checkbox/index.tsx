import { Field } from "formik";
import React from "react";

import type { ICheckboxProps } from "./CustomCheckbox";
import { CustomCheckbox } from "./CustomCheckbox";

const Checkbox: React.FC<ICheckboxProps> = ({
  disabled = false,
  id,
  label,
  name,
  value,
}: Readonly<ICheckboxProps>): JSX.Element => (
  <Field
    component={CustomCheckbox}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    value={value}
  />
);

export { Checkbox };

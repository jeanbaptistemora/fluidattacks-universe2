import { Field } from "formik";
import React from "react";

import type { ICheckboxProps } from "./CustomCheckbox";
import { CustomCheckbox } from "./CustomCheckbox";

const Checkbox: React.FC<ICheckboxProps> = ({
  disabled = false,
  id,
  initChecked = false,
  name,
  onChange,
}: Readonly<ICheckboxProps>): JSX.Element => (
  <Field
    component={CustomCheckbox}
    disabled={disabled}
    id={id}
    initChecked={initChecked}
    name={name}
    onChange={onChange}
  />
);

export { Checkbox };

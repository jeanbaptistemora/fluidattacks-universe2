import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { ISelectProps } from "./CustomSelect";
import { CustomSelect } from "./CustomSelect";

const Select: FC<ISelectProps> = ({
  children,
  disabled,
  id,
  label,
  name,
  onBlur,
  onFocus,
  onKeyDown,
  tooltip,
  variant,
}: Readonly<ISelectProps>): JSX.Element => (
  <Field
    component={CustomSelect}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    onBlur={onBlur}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    tooltip={tooltip}
    type={"text"}
    variant={variant}
  >
    {children}
  </Field>
);

export { Select };

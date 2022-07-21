import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { ISelectProps } from "../Formik";
import { FormikSelect } from "../Formik";

const Select: FC<ISelectProps> = ({
  children,
  disabled,
  id,
  label,
  name,
  onBlur,
  onFocus,
  onKeyDown,
  required,
  tooltip,
  variant,
}: Readonly<ISelectProps>): JSX.Element => (
  <Field
    component={FormikSelect}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    onBlur={onBlur}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    required={required}
    tooltip={tooltip}
    type={"text"}
    variant={variant}
  >
    {children}
  </Field>
);

export { Select };

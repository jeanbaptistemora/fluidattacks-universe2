import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputProps } from "./CustomInput";
import { CustomInput } from "./CustomInput";
import { Select } from "./Select";
import { TextArea } from "./TextArea";

const Input: FC<IInputProps> = ({
  childLeft,
  childRight,
  children,
  disabled = false,
  id,
  label,
  name,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  rows = 3,
  type = "text",
  variant = "solid",
}: Readonly<IInputProps>): JSX.Element => (
  <Field
    childLeft={childLeft}
    childRight={childRight}
    component={CustomInput}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    onBlur={onBlur}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    placeholder={placeholder}
    rows={rows}
    type={type}
    variant={variant}
  >
    {children}
  </Field>
);

export { Input, Select, TextArea };

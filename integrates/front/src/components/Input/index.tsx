import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputProps } from "./CustomInput";
import { CustomInput } from "./CustomInput";

const Input: FC<IInputProps> = ({
  childLeft,
  childRight,
  disabled = false,
  name,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  type = "text",
  variant = "solid",
}: Readonly<IInputProps>): JSX.Element => (
  <Field
    childLeft={childLeft}
    childRight={childRight}
    component={CustomInput}
    disabled={disabled}
    name={name}
    onBlur={onBlur}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    placeholder={placeholder}
    type={type}
    variant={variant}
  />
);

export { Input };

import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputProps } from "./CustomInput";
import { CustomInput } from "./CustomInput";
import { DatePicker } from "./DatePicker";
import { InputNumber } from "./InputNumber";
import { Label } from "./Label";
import { Select } from "./Select";
import { TextArea } from "./TextArea";

const Input: FC<IInputProps> = ({
  childLeft,
  childRight,
  disabled = false,
  id,
  label,
  name,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
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
    required={required}
    tooltip={tooltip}
    type={type}
    variant={variant}
  />
);

export { DatePicker, Input, InputNumber, Label, Select, TextArea };

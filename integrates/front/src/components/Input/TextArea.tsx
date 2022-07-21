import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { ITextAreaProps } from "./CustomTextArea";
import { CustomTextArea } from "./CustomTextArea";

const TextArea: FC<ITextAreaProps> = ({
  disabled,
  id,
  label,
  name,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  rows,
  variant,
}: Readonly<ITextAreaProps>): JSX.Element => (
  <Field
    component={CustomTextArea}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    onBlur={onBlur}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    placeholder={placeholder}
    rows={rows}
    variant={variant}
  />
);

export { TextArea };

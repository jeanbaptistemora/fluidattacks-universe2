import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { ITextAreaProps } from "../Formik/FormikTextArea";
import { FormikTextArea } from "../Formik/FormikTextArea";

const TextArea: FC<ITextAreaProps> = ({
  disabled,
  id,
  label,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  rows,
  variant,
}: Readonly<ITextAreaProps>): JSX.Element => (
  <Field
    component={FormikTextArea}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    onBlur={onBlur}
    onChange={onChange}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    placeholder={placeholder}
    required={required}
    rows={rows}
    variant={variant}
  />
);

export { TextArea };

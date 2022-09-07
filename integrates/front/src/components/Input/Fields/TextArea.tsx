/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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

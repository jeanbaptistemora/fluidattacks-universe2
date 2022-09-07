/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { ICheckboxProps } from "../Formik/FormikCheckbox";
import { FormikCheckbox } from "../Formik/FormikCheckbox";

const Checkbox: FC<ICheckboxProps> = ({
  checked,
  disabled,
  id,
  label,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  required,
  tooltip,
  value,
}: Readonly<ICheckboxProps>): JSX.Element => (
  <Field
    checked={checked}
    component={FormikCheckbox}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    onBlur={onBlur}
    onChange={onChange}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    required={required}
    tooltip={tooltip}
    type={"checkbox"}
    value={value}
  />
);

export type { ICheckboxProps };
export { Checkbox };

/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
 */
import { Checkbox } from "antd";
import type { FieldProps } from "formik";
import { ErrorMessage } from "formik";
import React from "react";

import { ValidationError } from "utils/forms/fields/styles";

interface ICheckboxProps extends FieldProps {
  children: React.ReactNode;
  disabled?: boolean;
  isChecked?: boolean;
  label: string;
}

export const FormikCheckbox: React.FC<ICheckboxProps> = (
  props: Readonly<ICheckboxProps>
): JSX.Element => {
  const { field, children, disabled = false, isChecked = false, label } = props;
  const { name } = field;

  return (
    <React.Fragment>
      {isChecked ? (
        <Checkbox
          aria-label={name}
          checked={true}
          disabled={disabled}
          // Best way to pass down props.
          // eslint-disable-next-line react/jsx-props-no-spreading
          {...props}
        >
          {` ${label}`}
        </Checkbox>
      ) : (
        <Checkbox
          aria-label={name}
          disabled={disabled}
          // Best way to pass down props.
          // eslint-disable-next-line react/jsx-props-no-spreading
          {...field}
        >
          {` ${label}`}
        </Checkbox>
      )}

      {children}
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};

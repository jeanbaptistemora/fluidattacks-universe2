/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { FieldProps, FormikHandlers } from "formik";
import { ErrorMessage } from "formik";
import React from "react";

import { StyledSelect, ValidationError } from "utils/forms/fields/styles";

interface IDropdownProps extends FieldProps<string, Record<string, string>> {
  children: React.ReactNode;
  customChange: FormikHandlers["handleChange"] | undefined;
  disabled: boolean | undefined;
}

const FormikDropdown: React.FC<IDropdownProps> = ({
  children,
  disabled = false,
  field,
  form,
  customChange,
}: IDropdownProps): JSX.Element => {
  const { name, onChange, value } = field;

  function handleChange(event: unknown): void {
    onChange(event);

    if (customChange !== undefined) {
      customChange(event);
    }
  }

  function handleBlur(): void {
    form.setFieldTouched(name, true);
  }

  return (
    <React.Fragment>
      <StyledSelect
        aria-label={name}
        disabled={disabled}
        name={name}
        onBlur={handleBlur}
        onChange={handleChange}
        value={value}
      >
        {children}
      </StyledSelect>
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};

export { FormikDropdown };

/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { FieldProps } from "formik";
import { ErrorMessage } from "formik";
import React from "react";

import { StyledInput, ValidationError } from "utils/forms/fields/styles";

interface ITextProps extends FieldProps<string, Record<string, string>> {
  disabled: boolean;
  id: string;
  max: number | string;
  min: number | string;
  placeholder: string;
  step: number | string | undefined;
  type: string;
  className: string;
  onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void;
  onKeyDown?: (event: React.KeyboardEvent<HTMLInputElement>) => void;
  onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void;
}

export const FormikText: React.FC<ITextProps> = ({
  className,
  onBlur: customBlur,
  onFocus,
  onKeyDown,
  disabled,
  field,
  id,
  max,
  min,
  placeholder,
  step,
  type,
}: Readonly<ITextProps>): JSX.Element => {
  const { name, onBlur, onChange, value } = field;

  function handleBlur(event: React.FocusEvent<HTMLInputElement>): void {
    onBlur(event);

    if (customBlur !== undefined) {
      customBlur(event);
    }
  }

  return (
    <React.Fragment>
      <StyledInput
        aria-label={name}
        autoComplete={"off"}
        // eslint-disable-next-line react/forbid-component-props
        className={className}
        disabled={disabled}
        id={id}
        max={max}
        min={min}
        name={name}
        onBlur={handleBlur}
        onChange={onChange}
        onFocus={onFocus}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
        step={step}
        type={type}
        value={value}
      />
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};

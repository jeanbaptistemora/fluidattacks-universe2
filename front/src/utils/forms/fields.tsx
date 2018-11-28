/* tslint:disable jsx-no-lambda
 * Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 */

import React from "react";
import { FormControl, FormControlProps, FormGroup } from "react-bootstrap";
/**
 * Disabling here is necessary because
 * there are currently no available type definitions for
 * neither this nor any other 3rd-party react phone input components
 */
// @ts-ignore
import ReactPhoneInput from "react-phone-input-2";
import { FormProps, WrappedFieldProps } from "redux-form";
import style from "./index.css";

type CustomFieldProps = FormProps<{}, {}, {}> & FormControlProps & WrappedFieldProps;

const renderError: ((arg1: string) => JSX.Element) = (msg: string): JSX.Element => (
  <span className={style.validationError}>{msg}</span>
);

export const textField: ((arg1: CustomFieldProps) => JSX.Element) =
  (fieldProps: CustomFieldProps): JSX.Element => (
    <div>
      <FormControl
        id={fieldProps.id}
        type={fieldProps.type}
        placeholder={fieldProps.placeholder}
        min={fieldProps.min}
        max={fieldProps.max}
        value={fieldProps.input.value}
        onChange={fieldProps.input.onChange}
        onBlur={fieldProps.input.onBlur}
        disabled={fieldProps.disabled}
      />
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </div>
  );

export const phoneNumberField: ((arg1: CustomFieldProps) => JSX.Element) =
  (fieldProps: CustomFieldProps): JSX.Element => (
    <ReactPhoneInput
      defaultCountry="co"
      inputClass="form-control"
      inputStyle={{ paddingLeft: "48px" }}
      inputExtraProps={{ type: "" }}
      onChange={fieldProps.input.onChange}
      value={fieldProps.input.value}
      {...fieldProps}
    />
  );

const handleDropdownChange: ((arg1: React.FormEvent<FormGroup>, arg2: CustomFieldProps) => void) =
  (event: React.FormEvent<FormGroup>, fieldProps: CustomFieldProps): void => {
    fieldProps.input.onChange((event.target as HTMLInputElement).value);
  };

export const dropdownField: ((arg1: CustomFieldProps) => JSX.Element) =
  (fieldProps: CustomFieldProps): JSX.Element => (
    <div>
      <FormControl
        componentClass="select"
        children={fieldProps.children}
        defaultValue={fieldProps.meta.initial}
        onChange={(event: React.FormEvent<FormGroup>): void => { handleDropdownChange(event, fieldProps); }}
      />
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </div>
  );

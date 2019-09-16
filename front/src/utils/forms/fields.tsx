/* tslint:disable jsx-no-lambda
 * Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 */

import _ from "lodash";
import React from "react";
import { Badge, ControlLabel, FormControl, FormControlProps, FormGroup, Glyphicon, HelpBlock } from "react-bootstrap";
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
  <HelpBlock id="validationError" className={style.validationError}>{msg}</HelpBlock>
);

const renderCharacterCount: ((text: string) => JSX.Element) = (text: string): JSX.Element => (
  <Badge pullRight={true} className={style.badge}>{text.length}</Badge>
);

type autocompleteFieldProps = CustomFieldProps & { suggestions: string[] };
export const autocompleteTextField: ((fieldProps: autocompleteFieldProps) => JSX.Element) = (
  fieldProps: autocompleteFieldProps,
): JSX.Element => {
  const filteredSuggestions: string[] = fieldProps.suggestions
    .filter((suggestion: string): boolean =>
      !_.isEmpty(fieldProps.input.value.trim()) && suggestion.includes(fieldProps.input.value));

  const renderSuggestion: ((suggestion: string) => JSX.Element) = (suggestion: string): JSX.Element => {
    const handleSuggestionClick: (() => void) = (): void => {
      fieldProps.input.onChange(suggestion);
    };

    return (
      <li onClick={handleSuggestionClick}><span>{suggestion}</span></li>
    );
  };

  const shouldRender: boolean = filteredSuggestions.length > 0 && filteredSuggestions[0] !== fieldProps.input.value;

  return (
    <div>
      <FormControl
        className={style.formControl}
        disabled={fieldProps.disabled}
        id={fieldProps.id}
        placeholder={fieldProps.placeholder}
        type={fieldProps.type}
        {...fieldProps.input}
      />
      {shouldRender ? <ul className={style.suggestionList}>{filteredSuggestions.map(renderSuggestion)}</ul> : undefined}
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </div>
  );
};

export const textField: ((arg1: CustomFieldProps) => JSX.Element) =
  (fieldProps: CustomFieldProps): JSX.Element => (
    <div>
      <FormControl
        className={style.formControl}
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
      inputClass={`${style.formControl} ${style.phone_number}`}
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
        className={style.formControl}
        componentClass="select"
        children={fieldProps.children}
        defaultValue={fieldProps.meta.initial}
        onChange={(event: React.FormEvent<FormGroup>): void => { handleDropdownChange(event, fieldProps); }}
      />
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </div>
  );

const handleFileChange: ((arg1: React.FormEvent<FormControl>, arg2: CustomFieldProps) => void) =
  (event: React.FormEvent<FormGroup>, fieldProps: CustomFieldProps): void => {
    const files: FileList | null = (event.target as HTMLInputElement).files;
    fieldProps.input.onChange(!_.isNil(files) ? files[0].name : "");
  };

export const fileInputField: ((arg1: CustomFieldProps) => JSX.Element) =
  (fieldProps: CustomFieldProps): JSX.Element => (
    <FormGroup controlId={fieldProps.id} className={style.text_center}>
      <FormControl
        target={fieldProps.target}
        className={`${style.inputfile} ${style.inputfile_evidence}`}
        type="file"
        accept={fieldProps.accept}
        name={fieldProps.name}
        onChange={(event: React.FormEvent<FormControl>): void => { handleFileChange(event, fieldProps); }}
        onClick={fieldProps.onClick}
      />
      <ControlLabel>
        <span>{fieldProps.input.value}</span>
        <strong>
          <Glyphicon glyph="search" /> Choose a file&hellip;
        </strong>
      </ControlLabel>
    </FormGroup>
  );

export const textAreaField: ((arg1: CustomFieldProps & { withCount?: boolean }) => JSX.Element) =
  (fieldProps: CustomFieldProps & { withCount?: boolean }): JSX.Element => (
    <div>
      <FormControl
        componentClass="textarea"
        {...fieldProps}
        {...fieldProps.input}
        className={`${style.formControl} ${fieldProps.className}`}
      />
      {fieldProps.withCount === true ? renderCharacterCount(fieldProps.input.value as string) : undefined}
      {(fieldProps.withCount === true && fieldProps.meta.error) ? <br /> : undefined}
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </div>
  );

export const dateField: ((arg1: CustomFieldProps) => JSX.Element) =
  (fieldProps: CustomFieldProps): JSX.Element => (
    <div>
      <FormControl
        className={style.formControl}
        id={fieldProps.id}
        type={"date"}
        selected={fieldProps.input.value}
        onChange={fieldProps.input.onChange}
        onBlur={fieldProps.input.onBlur}
        disabled={fieldProps.disabled}
        value={fieldProps.input.value}
      />
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </div>
  );

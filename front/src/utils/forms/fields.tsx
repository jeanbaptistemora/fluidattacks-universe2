import _ from "lodash";
import React from "react";
import {
  Badge, Checkbox, ControlLabel, FormControl, FormControlProps, FormGroup, Glyphicon, HelpBlock, InputGroup,
} from "react-bootstrap";
/**
 * Disabling here is necessary because
 * there are currently no available type definitions for
 * neither this nor any other 3rd-party react phone input components
 */
// @ts-ignore
import ReactPhoneInput from "react-phone-input-2";
import { WrappedFieldProps } from "redux-form";
import style from "./index.css";

type CustomFieldProps = WrappedFieldProps & FormControlProps;

const renderError: ((arg1: string) => JSX.Element) = (msg: string): JSX.Element => (
  <HelpBlock id="validationError" className={style.validationError}>{msg}</HelpBlock>
);

const renderCharacterCount: ((text: string) => JSX.Element) = (text: string): JSX.Element => (
  <Badge pullRight={true} className={style.badge}>{text.length}</Badge>
);

type autocompleteFieldProps = CustomFieldProps & { suggestions: string[] };
export const autocompleteTextField: React.FC<autocompleteFieldProps> = (
  fieldProps: autocompleteFieldProps,
): JSX.Element => {
  const filteredSuggestions: string[] = _.isEmpty(fieldProps.input.value.trim())
    ? []
    : fieldProps.suggestions.filter((suggestion: string): boolean =>
      suggestion
        .toLowerCase()
        .includes(fieldProps.input.value.toLowerCase()));

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
        autoComplete="off"
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

export const textField: React.FC<CustomFieldProps> =
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

export const phoneNumberField: React.FC<CustomFieldProps> =
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

export const dropdownField: React.FC<CustomFieldProps> = (fieldProps: CustomFieldProps): JSX.Element => {
  const handleDropdownChange: React.FormEventHandler<FormControl> = (event: React.FormEvent<FormControl>): void => {
    fieldProps.input.onChange((event.target as HTMLInputElement).value);
  };

  return (
    <div>
      <FormControl
        className={style.formControl}
        componentClass="select"
        children={fieldProps.children}
        defaultValue={fieldProps.meta.initial}
        onChange={handleDropdownChange}
      />
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </div>
  );
};

export const fileInputField: React.FC<CustomFieldProps> = (fieldProps: CustomFieldProps): JSX.Element => {
  const handleFileChange: React.FormEventHandler<FormControl> = (event: React.FormEvent<FormControl>): void => {
    const files: FileList | null = (event.target as HTMLInputElement).files;
    fieldProps.input.onChange(!_.isNil(files) ? files[0].name : "");
  };

  return (
    <FormGroup controlId={fieldProps.id} className={style.text_center}>
      <InputGroup>
        <FormControl
          target={fieldProps.target}
          className={`${style.inputfile} ${style.inputfile_evidence}`}
          type="file"
          accept={fieldProps.accept}
          name={fieldProps.name}
          onChange={handleFileChange}
          onClick={fieldProps.onClick}
        />
        <ControlLabel>
          <span>{fieldProps.input.value}</span>
          <strong>
            <Glyphicon glyph="search" /> Explore&hellip;
          </strong>
        </ControlLabel>
      </InputGroup>
    </FormGroup>
  );
};

export const textAreaField: React.FC<CustomFieldProps & { withCount?: boolean }> =
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

export const dateField: React.FC<CustomFieldProps> =
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
        value={fieldProps.input.value.split(" ")[0]}
      />
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </div>
  );

export const dateTimeField: React.FC<CustomFieldProps> = (fieldProps: CustomFieldProps): JSX.Element => (
  <React.Fragment>
    <FormControl className={style.formControl} id={fieldProps.id} type="datetime-local" {...fieldProps.input} />
    {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
  </React.Fragment>
);

export const checkboxField: React.FC<CustomFieldProps> = (fieldProps: CustomFieldProps): JSX.Element => (
  <React.Fragment>
    <Checkbox checked={fieldProps.input.value} children={fieldProps.children} {...fieldProps.input} />
    {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
  </React.Fragment>
);

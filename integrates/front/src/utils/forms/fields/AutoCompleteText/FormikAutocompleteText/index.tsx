import type { FieldProps } from "formik";
import { useField } from "formik";
import _ from "lodash";
import type { InputHTMLAttributes } from "react";
import React from "react";

import { SuggestionItem } from "./suggestionItem";

import { StyledInput, ValidationError } from "utils/forms/fields/styles";
import style from "utils/forms/index.css";

interface IAutocompleteTextProps
  extends FieldProps<string, Record<string, string>>,
    Omit<InputHTMLAttributes<HTMLInputElement>, "form"> {
  focus: boolean;
  suggestions: string[];
}

export const FormikAutocompleteText: React.FC<IAutocompleteTextProps> = ({
  disabled,
  field,
  focus,
  form,
  placeholder,
  suggestions,
}: IAutocompleteTextProps): JSX.Element => {
  const { name, onChange, value } = field;
  const { errors, touched } = form;
  const fieldTouched = Boolean(touched[name]);
  const error = errors[name];
  const [, , helpers] = useField(name);

  const matches = suggestions.filter(
    (suggestion: string): boolean =>
      !_.isNil(value) &&
      value.trim() !== "" &&
      suggestion.toLowerCase().includes(value.toLowerCase())
  );

  function handleClick(newValue: string): void {
    helpers.setValue(newValue);
  }

  return (
    <React.Fragment>
      <StyledInput
        autoComplete={"off"}
        autoFocus={focus} // eslint-disable-line jsx-a11y/no-autofocus
        disabled={disabled}
        name={name}
        onChange={onChange}
        placeholder={placeholder}
        type={"text"}
        value={value}
      />
      {matches.length > 0 && matches[0] !== value ? (
        <ul className={style.suggestionList}>
          {matches.map(
            (match: string): JSX.Element => (
              <SuggestionItem
                key={match}
                onChange={handleClick}
                value={match}
              />
            )
          )}
        </ul>
      ) : undefined}
      {fieldTouched && error !== undefined ? (
        <ValidationError id={"validationError"}>{error}</ValidationError>
      ) : undefined}
    </React.Fragment>
  );
};

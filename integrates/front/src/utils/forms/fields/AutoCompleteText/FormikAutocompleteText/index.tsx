import type { FieldProps } from "formik";
import type { InputHTMLAttributes } from "react";
import React from "react";

import { SuggestionItem } from "./suggestionItem";

import { StyledInput, ValidationError } from "utils/forms/fields/styles";

interface IAutocompleteTextProps
  extends FieldProps<string, Record<string, string>>,
    Omit<InputHTMLAttributes<HTMLInputElement>, "form"> {
  suggestions: string[];
}

export const FormikAutocompleteText: React.FC<IAutocompleteTextProps> = ({
  disabled,
  field,
  form,
  suggestions,
}: IAutocompleteTextProps): JSX.Element => {
  const { name, onChange, value } = field;
  const { errors, touched } = form;
  const fieldTouched = Boolean(touched[name]);
  const error = errors[name];

  const matches = suggestions.filter(
    (suggestion: string): boolean =>
      value.trim() !== "" &&
      suggestion.toLowerCase().includes(value.toLowerCase())
  );

  return (
    <React.Fragment>
      <StyledInput
        autoComplete={"off"}
        disabled={disabled}
        name={name}
        onChange={onChange}
        type={"text"}
        value={value}
      />
      {matches.length > 0 && matches[0] !== value ? (
        <ul>
          {matches.map(
            (match: string): JSX.Element => (
              <SuggestionItem key={match} onChange={onChange} value={match} />
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

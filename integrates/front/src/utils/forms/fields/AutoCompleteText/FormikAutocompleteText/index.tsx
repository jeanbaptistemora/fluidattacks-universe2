import type { FieldProps } from "formik";
import type { InputHTMLAttributes } from "react";
import React from "react";

import { SuggestionItem } from "./suggestionItem";

import { ValidationError } from "styles/styledComponents";

interface IAutocompleteTextProps
  extends FieldProps<string, Record<string, string>>,
    Omit<InputHTMLAttributes<HTMLInputElement>, "form"> {
  suggestions: string[];
}

export const AutocompleteText: React.FC<IAutocompleteTextProps> = ({
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
      <input autoComplete={"off"} disabled={disabled} type={"text"} />
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

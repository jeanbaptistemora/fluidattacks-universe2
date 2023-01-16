import type { FieldProps } from "formik";
import type { InputHTMLAttributes } from "react";
import React from "react";

import { StyledInput, ValidationError } from "utils/forms/fields/styles";

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
  const { errors } = form;
  const error = errors[name];

  return (
    <React.Fragment>
      <StyledInput
        aria-label={name}
        autoComplete={"off"}
        autoFocus={focus} // eslint-disable-line jsx-a11y/no-autofocus
        disabled={disabled}
        list={`${name}-list`}
        name={name}
        onChange={onChange}
        placeholder={placeholder}
        type={"text"}
        value={value}
      />
      <datalist id={`${name}-list`}>
        {suggestions.map(
          (suggestion: string): JSX.Element => (
            <option key={suggestion} value={suggestion} />
          )
        )}
      </datalist>
      <ValidationError id={"validationError"}>{error}</ValidationError>
    </React.Fragment>
  );
};

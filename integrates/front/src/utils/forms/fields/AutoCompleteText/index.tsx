/* eslint-disable react/forbid-component-props
  -------
  We need it to override default styles from react-bootstrap.
*/
import React from "react";
import { ValidationError } from "styles/styledComponents";
import _ from "lodash";
import style from "utils/forms/index.css";
import type { WrappedFieldInputProps, WrappedFieldProps } from "redux-form";

interface IAutoCompleteTextProps extends WrappedFieldProps {
  autoComplete?: string;
  className?: string;
  disabled?: boolean;
  id?: string;
  input: Omit<WrappedFieldInputProps, "value"> & { value: string };
  placeholder?: string;
  suggestions: string[];
  type: string;
}

export const AutoCompleteText: React.FC<IAutoCompleteTextProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<IAutoCompleteTextProps>
): JSX.Element => {
  const { input, suggestions, disabled, id, placeholder, type, meta } = props;
  const { value, onChange } = input;

  const filteredSuggestions: string[] = _.isEmpty(value.trim())
    ? []
    : suggestions.filter((suggestion: string): boolean =>
        suggestion.toLowerCase().includes(value.toLowerCase())
      );

  const shouldRender: boolean =
    filteredSuggestions.length > 0 && filteredSuggestions[0] !== value;

  return (
    <React.Fragment>
      <input
        autoComplete={"off"}
        className={style["form-control"]}
        disabled={disabled}
        id={id}
        placeholder={placeholder}
        type={type}
        // Best way to pass down props
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...input}
      />
      {shouldRender && (
        <ul className={style.suggestionList}>
          {filteredSuggestions.map(
            (suggestion: string): JSX.Element => {
              function handleSuggestionClick(): void {
                onChange(suggestion);
              }

              return (
                <button
                  key={suggestion}
                  onClick={handleSuggestionClick}
                  type={"button"}
                >
                  <li>{suggestion}</li>
                </button>
              );
            }
          )}
        </ul>
      )}
      {meta.touched && !_.isUndefined(meta.error) && (
        <ValidationError id={"validationError"}>
          {meta.error as string}
        </ValidationError>
      )}
    </React.Fragment>
  );
};

/* eslint-disable react/forbid-component-props
  -------
  We need it to override default styles from react-bootstrap
*/
import React from "react";
import _ from "lodash";
import { default as style } from "../../index.css";
import { FormControl, FormControlProps, HelpBlock } from "react-bootstrap";
import { WrappedFieldInputProps, WrappedFieldProps } from "redux-form";

interface IAutoCompleteTextProps extends WrappedFieldProps, FormControlProps {
  input: { value: string } & Omit<WrappedFieldInputProps, "value">;
  suggestions: string[];
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
    <div>
      <FormControl
        autoComplete={"off"}
        className={style.formControl}
        disabled={disabled}
        id={id}
        placeholder={placeholder}
        type={type}
        // Best way to pass down
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...input}
      />
      {shouldRender ? (
        <ul className={style.suggestionList}>
          {filteredSuggestions.map(
            (suggestion: string): JSX.Element => {
              function handleSuggestionClick(): void {
                onChange(suggestion);
              }

              return (
                <li key={suggestion} onClick={handleSuggestionClick}>
                  <span>{suggestion}</span>
                </li>
              );
            }
          )}
        </ul>
      ) : undefined}
      {meta.touched && !_.isUndefined(meta.error) && (
        <HelpBlock className={style.validationError} id={"validationError"}>
          {meta.error as string}
        </HelpBlock>
      )}
    </div>
  );
};

import type { FieldProps } from "formik";
import { ErrorMessage } from "formik";
import React, { useCallback } from "react";
import TextArea from "react-textarea-autosize";

import { ValidationError } from "utils/forms/fields/styles";

interface ITextProps extends FieldProps<string, Record<string, string>> {
  disabled: boolean;
  id: string;
  maxRows: number;
  minRows: number;
  placeholder: string;
  type: string;
  onTextChange: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onFocus: () => void;
}

export const FormikTextAreaAutosize: React.FC<ITextProps> = ({
  disabled,
  field,
  id,
  maxRows,
  minRows,
  onTextChange,
  onFocus,
  placeholder,
  type,
}: ITextProps): JSX.Element => {
  const { name, onChange, value } = field;

  const onChangeText = useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
      onTextChange(event);
      onChange(event);
    },
    [onChange, onTextChange]
  );

  return (
    <React.Fragment>
      <TextArea
        aria-label={name}
        // eslint-disable-next-line jsx-a11y/no-autofocus
        autoFocus={true}
        disabled={disabled}
        id={id}
        maxRows={maxRows}
        minRows={minRows}
        name={name}
        onChange={onChangeText}
        onFocus={onFocus}
        placeholder={placeholder}
        type={type}
        value={value}
      />
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};

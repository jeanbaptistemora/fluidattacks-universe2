import type { FieldProps } from "formik";
import type { FC, FocusEvent } from "react";
import React, { useCallback } from "react";

import type { IInputBase } from "../InputBase";
import { InputBase } from "../InputBase";
import { StyledTextArea } from "../styles";

interface ITextAreaProps extends IInputBase<HTMLTextAreaElement> {
  placeholder?: string;
  rows?: number;
}

type TTextAreaProps = FieldProps<string, Record<string, string>> &
  ITextAreaProps;

const FormikTextArea: FC<TTextAreaProps> = ({
  disabled,
  field,
  form,
  id,
  label,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  rows = 3,
  tooltip,
  variant,
}: Readonly<TTextAreaProps>): JSX.Element => {
  const { name, onBlur: onBlurField, onChange, value } = field;
  const alert = form.errors[name];

  const handleBlur = useCallback(
    (ev: FocusEvent<HTMLTextAreaElement>): void => {
      onBlurField(ev);
      onBlur?.(ev);
    },
    [onBlur, onBlurField]
  );

  return (
    <InputBase
      alert={alert}
      id={id}
      label={label}
      name={name}
      required={required}
      tooltip={tooltip}
      variant={variant}
    >
      <StyledTextArea
        aria-label={name}
        autoComplete={"off"}
        disabled={disabled}
        id={id}
        name={name}
        onBlur={handleBlur}
        onChange={onChange}
        onFocus={onFocus}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
        rows={rows}
        value={value}
      />
    </InputBase>
  );
};

export type { ITextAreaProps };
export { FormikTextArea };

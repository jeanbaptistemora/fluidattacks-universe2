import type { FieldProps } from "formik";
import React, { useCallback } from "react";

import type { IStyledInputProps } from "./styles";
import { InputBox, InputWrapper, StyledInput } from "./styles";

import { Alert } from "components/Alert";

interface IInputProps extends Partial<IStyledInputProps> {
  childLeft?: React.ReactNode;
  childRight?: React.ReactNode;
  disabled?: boolean;
  name: string;
  onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void;
  onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void;
  onKeyDown?: (event: React.KeyboardEvent<HTMLInputElement>) => void;
  placeholder?: string;
  type?: "email" | "password" | "text";
}

const CustomInput: React.FC<
  FieldProps<string, Record<string, string>> & IInputProps
> = ({
  childLeft,
  childRight,
  disabled,
  field,
  form,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  type,
  variant = "solid",
}: Readonly<
  FieldProps<string, Record<string, string>> & IInputProps
>): JSX.Element => {
  const { name, onBlur: onBlurField, onChange, value } = field;
  const alert = form.errors[name] ?? "";

  const handleBlur = useCallback(
    (ev: React.FocusEvent<HTMLInputElement>): void => {
      onBlurField(ev);
      onBlur?.(ev);
    },
    [onBlur, onBlurField]
  );

  return (
    <InputBox showAlert={alert.length > 0}>
      <InputWrapper variant={variant}>
        {childLeft}
        <StyledInput
          aria-label={name}
          autoComplete={"off"}
          disabled={disabled}
          name={name}
          onBlur={handleBlur}
          onChange={onChange}
          onFocus={onFocus}
          onKeyDown={onKeyDown}
          placeholder={placeholder}
          type={type}
          value={value}
        />
        {childRight}
      </InputWrapper>
      <Alert icon={true} variant={"error"}>
        {alert}
      </Alert>
    </InputBox>
  );
};

export type { IInputProps };
export { CustomInput };

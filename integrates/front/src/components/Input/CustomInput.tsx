import type { FieldProps } from "formik";
import React, { useCallback } from "react";

import type { IStyledInputProps } from "./styles";
import {
  InputBox,
  InputWrapper,
  StyledInput,
  StyledSelect,
  StyledTextArea,
} from "./styles";

import { Alert } from "components/Alert";
import { Text } from "components/Text";

interface IInputProps extends Partial<IStyledInputProps> {
  childLeft?: React.ReactNode;
  childRight?: React.ReactNode;
  children?: React.ReactNode;
  disabled?: boolean;
  id?: string;
  label?: React.ReactNode;
  name: string;
  onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void;
  onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void;
  onKeyDown?: (event: React.KeyboardEvent<HTMLInputElement>) => void;
  placeholder?: string;
  rows?: number;
  type?: "email" | "password" | "select" | "text" | "textarea";
}

const CustomInput: React.FC<
  FieldProps<string, Record<string, string>> & IInputProps
> = ({
  childLeft,
  childRight,
  children,
  disabled,
  field,
  form,
  id,
  label,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  rows = 3,
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
      {label === undefined ? undefined : (
        <label htmlFor={id}>
          <Text mb={1}>{label}</Text>
        </label>
      )}
      <InputWrapper variant={variant}>
        {childLeft}
        {type === "select" ? (
          <StyledSelect
            aria-label={name}
            autoComplete={"off"}
            disabled={disabled}
            id={id}
            name={name}
            onChange={onChange}
            value={value}
          >
            {children}
          </StyledSelect>
        ) : type === "textarea" ? (
          <StyledTextArea
            aria-label={name}
            autoComplete={"off"}
            disabled={disabled}
            id={id}
            name={name}
            onChange={onChange}
            placeholder={placeholder}
            rows={rows}
            value={value}
          />
        ) : (
          <StyledInput
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
            type={type}
            value={value}
          />
        )}
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

import { faCircleXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FieldProps } from "formik";
import React, { useCallback } from "react";

import type { IAlertProps, IStyledInputProps } from "./styles";
import { Alert, Container, StyledInput } from "./styles";

interface IInputProps extends Partial<IStyledInputProps> {
  alertType?: IAlertProps["variant"];
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
  alertType = "low",
  disabled = false,
  field,
  form,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  type = "text",
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
    <Container>
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
        variant={variant}
      />
      <Alert show={alert.length > 0} variant={alertType}>
        <FontAwesomeIcon icon={faCircleXmark} />
        &nbsp;
        {alert}
      </Alert>
    </Container>
  );
};

export type { IInputProps };
export { CustomInput };

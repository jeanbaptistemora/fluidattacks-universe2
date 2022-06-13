import { faCircleXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FieldProps, FormikHandlers } from "formik";
import React, { useCallback } from "react";

import type { IAlertProps, IStyledInputProps } from "./styles";
import { Alert, Container, StyledInput } from "./styles";

interface IInputProps extends Partial<IStyledInputProps> {
  alertType?: IAlertProps["variant"];
  customKeyDown?: (event: React.KeyboardEvent<HTMLInputElement>) => void;
  customBlur?: FormikHandlers["handleBlur"];
  disabled?: boolean;
  name: string;
  placeholder?: string;
  type?: "email" | "password" | "text";
}

const CustomInput: React.FC<
  FieldProps<string, Record<string, string>> & IInputProps
> = ({
  alertType = "low",
  customBlur,
  customKeyDown,
  disabled = false,
  field,
  form,
  placeholder,
  type = "text",
  variant = "solid",
}: Readonly<
  FieldProps<string, Record<string, string>> & IInputProps
>): JSX.Element => {
  const { name, onBlur, onChange, value } = field;
  const alert = form.errors[name] ?? "";

  const handleBlur = useCallback(
    (ev: unknown): void => {
      onBlur(ev);
      customBlur?.(ev);
    },
    [customBlur, onBlur]
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
        onKeyDown={customKeyDown}
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

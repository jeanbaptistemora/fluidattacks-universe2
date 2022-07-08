import type { FieldProps } from "formik";
import type { FC, FocusEvent, KeyboardEvent, ReactNode } from "react";
import React, { useCallback } from "react";

import type { IInputBase } from "./InputBase";
import { InputBase } from "./InputBase";
import { StyledInput } from "./styles";

interface IInputProps extends IInputBase {
  childLeft?: ReactNode;
  childRight?: ReactNode;
  onBlur?: (event: FocusEvent<HTMLInputElement>) => void;
  onFocus?: (event: FocusEvent<HTMLInputElement>) => void;
  onKeyDown?: (event: KeyboardEvent<HTMLInputElement>) => void;
  placeholder?: string;
  type?: "email" | "password" | "text";
}

type TInputProps = FieldProps<string, Record<string, string>> & IInputProps;

const CustomInput: FC<TInputProps> = ({
  childLeft,
  childRight,
  disabled,
  field,
  form,
  id,
  label,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  type,
  variant = "solid",
}: Readonly<TInputProps>): JSX.Element => {
  const { name, onBlur: onBlurField, onChange, value } = field;
  const alert = form.errors[name];

  const handleBlur = useCallback(
    (ev: FocusEvent<HTMLInputElement>): void => {
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
      variant={variant}
    >
      {childLeft}
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
      {childRight}
    </InputBase>
  );
};

export type { IInputProps };
export { CustomInput };

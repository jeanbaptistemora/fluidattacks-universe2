import type { FieldProps } from "formik";
import type { FC, FocusEvent, ReactNode } from "react";
import React, { useCallback } from "react";

import type { IInputBase } from "./InputBase";
import { InputBase } from "./InputBase";
import { StyledInput } from "./styles";

interface IInputProps extends IInputBase<HTMLInputElement> {
  childLeft?: ReactNode;
  childRight?: ReactNode;
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
  tooltip,
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
      tooltip={tooltip}
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

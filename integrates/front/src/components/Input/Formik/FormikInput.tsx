import type { FC, FocusEvent, ReactNode } from "react";
import React, { useCallback } from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase } from "../InputBase";
import { StyledInput } from "../styles";

interface IInputProps extends IInputBase<HTMLInputElement> {
  childLeft?: ReactNode;
  childRight?: ReactNode;
  placeholder?: string;
  type?: "email" | "password" | "text";
}

type TInputProps = IInputProps & TFieldProps;

const FormikInput: FC<TInputProps> = ({
  childLeft,
  childRight,
  disabled,
  field: { name, onBlur: onBlurField, onChange, value },
  form,
  id,
  label,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
  type,
  variant = "solid",
}: Readonly<TInputProps>): JSX.Element => {
  const handleBlur = useCallback(
    (ev: FocusEvent<HTMLInputElement>): void => {
      onBlurField(ev);
      onBlur?.(ev);
    },
    [onBlur, onBlurField]
  );

  return (
    <InputBase
      form={form}
      id={id}
      label={label}
      name={name}
      required={required}
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
export { FormikInput };

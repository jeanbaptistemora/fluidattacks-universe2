import type { FC, ReactNode } from "react";
import React from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase, useHandlers } from "../InputBase";
import { StyledInput } from "../styles";

interface IInputProps extends IInputBase<HTMLInputElement> {
  childLeft?: ReactNode;
  childRight?: ReactNode;
  list?: string;
  placeholder?: string;
  value?: number | string;
  type?: "email" | "number" | "password" | "text";
}

type TInputProps = IInputProps & TFieldProps;

const FormikInput: FC<TInputProps> = ({
  childLeft,
  childRight,
  disabled,
  field: { name, onBlur: fieldBlur, onChange: fieldChange, value },
  form,
  id,
  label,
  list,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  onPaste,
  placeholder,
  required,
  tooltip,
  type,
  variant = "solid",
}: Readonly<TInputProps>): JSX.Element => {
  const [handleBlur, handleChange] = useHandlers(
    { onBlur: fieldBlur, onChange: fieldChange },
    { onBlur, onChange }
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
        id={label === undefined ? id : id ?? name}
        list={list}
        name={name}
        onBlur={handleBlur}
        onChange={handleChange}
        onFocus={onFocus}
        onKeyDown={onKeyDown}
        onPaste={onPaste}
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

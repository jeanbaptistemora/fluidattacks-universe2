import type { FC } from "react";
import React from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase, useHandlers } from "../InputBase";
import { StyledInput } from "../styles";

interface IInputDateProps extends IInputBase<HTMLInputElement> {
  max?: string;
  min?: string;
}

type TInputDateProps = IInputDateProps & TFieldProps;

const FormikDate: FC<TInputDateProps> = ({
  disabled = false,
  field: { name, onBlur: fieldBlur, onChange: fieldChange, value },
  form,
  id,
  label,
  max,
  min,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
  variant = "solid",
}: Readonly<TInputDateProps>): JSX.Element => {
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
      <StyledInput
        aria-label={name}
        autoComplete={"off"}
        disabled={disabled}
        id={id}
        max={max}
        min={min}
        name={name}
        onBlur={handleBlur}
        onChange={handleChange}
        onFocus={onFocus}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
        type={"date"}
        value={value}
      />
    </InputBase>
  );
};

export type { IInputDateProps };
export { FormikDate };
